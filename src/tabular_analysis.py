"""Reusable statistical and preprocessing helpers for Adult Census Income."""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
from scipy.stats import ks_2samp
from sklearn.experimental import enable_iterative_imputer  # noqa: F401
from sklearn.impute import IterativeImputer, KNNImputer, SimpleImputer
from sklearn.linear_model import BayesianRidge
from sklearn.preprocessing import StandardScaler

RANDOM_SEED = 42


def split_feature_types(frame: pd.DataFrame, target: str = "income"):
    X = frame.drop(columns=[target]).copy()
    numeric = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical = [c for c in X.columns if c not in numeric]
    return X, numeric, categorical


def little_mcar_test(frame: pd.DataFrame, target: str = "income") -> float:
    """Run Little's MCAR test via pyampute after documented ordinal coding.

    This is an exploratory implementation: categorical values are ordinal-coded
    because Little's test is a numeric multivariate-normal test. Interpret cautiously.
    """
    from pyampute.exploration.mcar_statistical_tests import MCARTest

    X = frame.drop(columns=[target], errors="ignore").copy()
    for col in X.columns:
        if not pd.api.types.is_numeric_dtype(X[col]):
            categorical = pd.Categorical(X[col])
            codes = pd.Series(categorical.codes, index=X.index, dtype="float64")
            codes.loc[codes == -1] = np.nan
            X[col] = codes
    X = X.replace([np.inf, -np.inf], np.nan).astype(float)
    if not X.isna().any().any():
        raise ValueError("Little's MCAR test cần dữ liệu có giá trị thiếu.")
    return float(MCARTest(method="little").little_mcar_test(X))


def compare_numeric_imputers(
    frame: pd.DataFrame,
    numeric_columns: list[str],
    missing_rate: float = 0.10,
    random_state: int = RANDOM_SEED,
) -> pd.DataFrame:
    """Benchmark mean/median/mode, KNN k=3/5/10 and MICE using artificial MCAR.

    Only originally complete numerical cells are used for RMSE. Categorical
    variables are imputed separately with most-frequent values in model pipelines.
    """
    from sklearn.metrics import root_mean_squared_error

    complete = frame[numeric_columns].dropna().copy()
    if len(complete) < 100:
        raise ValueError("Không đủ dòng numeric complete để benchmark imputation.")
    # A reproducible cap prevents excessive runtime on lower-memory laptops.
    if len(complete) > 12_000:
        complete = complete.sample(12_000, random_state=random_state)
    truth = complete.to_numpy(dtype=float)
    rng = np.random.default_rng(random_state)
    mask = rng.random(truth.shape) < missing_rate
    corrupted = truth.copy()
    corrupted[mask] = np.nan
    results = []

    simple_methods = {
        "Mean": SimpleImputer(strategy="mean"),
        "Median": SimpleImputer(strategy="median"),
        "Mode": SimpleImputer(strategy="most_frequent"),
    }
    for name, imputer in simple_methods.items():
        restored = imputer.fit_transform(corrupted)
        results.append({"method": name, "RMSE": float(root_mean_squared_error(truth[mask], restored[mask]))})

    scaler = StandardScaler()
    corrupted_scaled = scaler.fit_transform(corrupted)
    for k in (3, 5, 10):
        restored_scaled = KNNImputer(n_neighbors=k, weights="distance").fit_transform(corrupted_scaled)
        restored = scaler.inverse_transform(restored_scaled)
        results.append({"method": f"KNN (k={k})", "RMSE": float(root_mean_squared_error(truth[mask], restored[mask]))})

    mice = IterativeImputer(
        estimator=BayesianRidge(), max_iter=10, initial_strategy="median",
        random_state=random_state, skip_complete=True
    )
    restored = mice.fit_transform(corrupted)
    results.append({"method": "MICE / IterativeImputer", "RMSE": float(root_mean_squared_error(truth[mask], restored[mask]))})
    return pd.DataFrame(results).sort_values("RMSE").reset_index(drop=True)


def detect_outliers(frame: pd.DataFrame, numeric_columns: list[str], random_state: int = RANDOM_SEED):
    """Compare IQR, Z-score, Isolation Forest, LOF and DBSCAN outlier masks."""
    from sklearn.cluster import DBSCAN
    from sklearn.decomposition import PCA
    from sklearn.ensemble import IsolationForest
    from sklearn.neighbors import LocalOutlierFactor
    from sklearn.preprocessing import RobustScaler, StandardScaler

    data = frame[numeric_columns].dropna().copy()
    if len(data) > 6_000:
        data = data.sample(6_000, random_state=random_state)
    values = data.to_numpy(dtype=float)
    masks: dict[str, np.ndarray] = {}

    q1 = np.nanpercentile(values, 25, axis=0)
    q3 = np.nanpercentile(values, 75, axis=0)
    iqr = q3 - q1
    masks["IQR"] = ((values < q1 - 1.5 * iqr) | (values > q3 + 1.5 * iqr)).any(axis=1)

    z = np.abs((values - np.mean(values, axis=0)) / np.where(np.std(values, axis=0) == 0, 1, np.std(values, axis=0)))
    masks["Z-score |z|>3"] = (z > 3).any(axis=1)

    scaled = RobustScaler().fit_transform(values)
    for contamination in (0.01, 0.05, 0.10):
        model = IsolationForest(contamination=contamination, random_state=random_state, n_estimators=150, n_jobs=-1)
        masks[f"Isolation Forest ({contamination})"] = model.fit_predict(scaled) == -1
    for neighbors in (10, 20, 50):
        model = LocalOutlierFactor(n_neighbors=neighbors, contamination=0.05, n_jobs=-1)
        masks[f"LOF ({neighbors})"] = model.fit_predict(scaled) == -1

    reduced = PCA(n_components=min(5, scaled.shape[1]), random_state=random_state).fit_transform(scaled)
    # eps is stated explicitly and must be interpreted as a tunable DBSCAN choice.
    dbscan_labels = DBSCAN(eps=2.2, min_samples=10, n_jobs=-1).fit_predict(reduced)
    masks["DBSCAN noise"] = dbscan_labels == -1

    summary = pd.DataFrame([
        {"method": name, "outlier_count": int(mask.sum()), "outlier_rate": float(mask.mean())}
        for name, mask in masks.items()
    ]).sort_values("outlier_rate", ascending=False)
    index = list(masks)
    jaccard = pd.DataFrame(index=index, columns=index, dtype=float)
    for a in index:
        for b in index:
            union = np.logical_or(masks[a], masks[b]).sum()
            intersection = np.logical_and(masks[a], masks[b]).sum()
            jaccard.loc[a, b] = float(intersection / union) if union else 1.0
    return data, masks, summary, jaccard


def ks_before_after_outlier_removal(data: pd.DataFrame, outlier_mask: np.ndarray, numeric_columns: list[str]):
    """Descriptive KS comparisons; the samples are nested, not independent."""
    rows = []
    kept = data.loc[~outlier_mask]
    for col in numeric_columns:
        stat, pvalue = ks_2samp(data[col].dropna(), kept[col].dropna())
        rows.append({"feature": col, "KS_statistic": float(stat), "p_value": float(pvalue)})
    return pd.DataFrame(rows)


def binary_target(series: pd.Series) -> pd.Series:
    clean = series.astype("string").str.strip().str.rstrip(".")
    mapping = {"<=50K": 0, ">50K": 1}
    mapped = clean.map(mapping)
    if mapped.isna().any():
        bad = clean[mapped.isna()].unique().tolist()
        raise ValueError(f"Income labels غير معروفة: {bad}")
    return mapped.astype(int)


def make_preprocessor(numeric_columns, categorical_columns, numeric_scaler="standard", minmax=False):
    """Leakage-safe ColumnTransformer for mixed tabular features."""
    from sklearn.compose import ColumnTransformer
    from sklearn.impute import SimpleImputer
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, RobustScaler, StandardScaler

    if minmax:
        scaler = MinMaxScaler()
    elif numeric_scaler == "robust":
        scaler = RobustScaler()
    else:
        scaler = StandardScaler()
    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", scaler),
    ])
    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", drop="first")),
    ])
    return ColumnTransformer([
        ("numeric", numeric_pipeline, numeric_columns),
        ("categorical", categorical_pipeline, categorical_columns),
    ], remainder="drop")


def encode_variants(X_train: pd.DataFrame, X_test: pd.DataFrame, categorical_columns: list[str], y_train):
    """Create one-hot, ordinal, target, binary and frequency encodings.

    TargetEncoder.fit_transform performs internal cross-fitting on the training set.
    All mappings are learned from training data only and then applied to test data.
    """
    from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, TargetEncoder

    train_cat = X_train[categorical_columns].fillna("__MISSING__").astype(str)
    test_cat = X_test[categorical_columns].fillna("__MISSING__").astype(str)
    outputs = {}

    onehot = OneHotEncoder(handle_unknown="ignore", drop=None, sparse_output=True)
    outputs["One-Hot"] = (onehot.fit_transform(train_cat), onehot.transform(test_cat), onehot.get_feature_names_out(categorical_columns))

    ordinal = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
    outputs["Ordinal"] = (ordinal.fit_transform(train_cat), ordinal.transform(test_cat), np.array(categorical_columns))

    target_encoder = TargetEncoder(target_type="binary", smooth="auto", cv=5, shuffle=True, random_state=RANDOM_SEED)
    outputs["Target (cross-fit)"] = (
        target_encoder.fit_transform(train_cat, y_train),
        target_encoder.transform(test_cat),
        np.array(categorical_columns),
    )

    binary_train, binary_test, binary_names = [], [], []
    # Binary encoding is reserved for high-cardinality categorical columns (>20 values).
    high_cardinality = [col for col in categorical_columns if train_cat[col].nunique(dropna=True) > 20]
    for col in high_cardinality:
        categories = pd.Index(train_cat[col].unique())
        lookup = {value: idx for idx, value in enumerate(categories)}
        unknown_code = len(lookup)
        n_bits = max(1, int(np.ceil(np.log2(max(len(categories) + 1, 2)))))
        train_codes = train_cat[col].map(lookup).fillna(unknown_code).astype(int).to_numpy()
        test_codes = test_cat[col].map(lookup).fillna(unknown_code).astype(int).to_numpy()
        for bit in range(n_bits):
            binary_train.append((train_codes >> bit) & 1)
            binary_test.append((test_codes >> bit) & 1)
            binary_names.append(f"{col}_bin_{bit}")
    if binary_train:
        binary_train_matrix = np.column_stack(binary_train)
        binary_test_matrix = np.column_stack(binary_test)
    else:
        binary_train_matrix = np.empty((len(X_train), 0), dtype=np.int8)
        binary_test_matrix = np.empty((len(X_test), 0), dtype=np.int8)
    outputs["Binary"] = (binary_train_matrix, binary_test_matrix, np.array(binary_names))

    frequency_train, frequency_test, frequency_names = [], [], []
    for col in categorical_columns:
        freq = train_cat[col].value_counts(normalize=True)
        frequency_train.append(train_cat[col].map(freq).fillna(0).to_numpy())
        frequency_test.append(test_cat[col].map(freq).fillna(0).to_numpy())
        frequency_names.append(f"{col}_frequency")
    outputs["Frequency"] = (np.column_stack(frequency_train), np.column_stack(frequency_test), np.array(frequency_names))
    return outputs

