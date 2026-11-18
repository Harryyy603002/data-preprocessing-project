"""Reproducible loaders for the public Hugging Face datasets used in this project."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

ADULT_DATASET_ID = "scikit-learn/adult-census-income"
CIFAR10_DATASET_ID = "uoft-cs/cifar10"
RANDOM_SEED = 42


def project_root() -> Path:
    """Return the repository root, independent of the notebook working directory."""
    here = Path(__file__).resolve()
    return here.parent.parent


def configure_huggingface_cache() -> Path:
    """Keep Hugging Face downloads outside Git-tracked source files."""
    cache_dir = project_root() / "data" / "raw" / ".hf_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("HF_HOME", str(cache_dir))
    return cache_dir


def _load_hf_dataset(dataset_id: str, **kwargs: Any):
    configure_huggingface_cache()
    try:
        from datasets import load_dataset
    except ImportError as exc:  # pragma: no cover - depends on local environment
        raise ImportError(
            "Thiếu thư viện 'datasets'. Hãy chạy: python -m pip install -r requirements.txt"
        ) from exc
    return load_dataset(dataset_id, **kwargs)


def load_adult_dataset() -> pd.DataFrame:
    """Load Adult Census Income and normalize missing markers/column names.

    The source contains 32,561 rows and 14 predictor columns plus the income label.
    The literal '?' marker is converted to np.nan before any analysis.
    """
    dataset = _load_hf_dataset(ADULT_DATASET_ID, split="train")
    frame = dataset.to_pandas()
    frame.columns = [
        str(col).strip().lower().replace(".", "_").replace("-", "_").replace(" ", "_")
        for col in frame.columns
    ]
    for col in frame.select_dtypes(include=["object", "string"]).columns:
        frame[col] = frame[col].astype("string").str.strip()
        frame[col] = frame[col].replace({"?": pd.NA, "": pd.NA})

    # Normalize target labels without changing the original two-class task.
    if "income" not in frame.columns:
        candidates = [c for c in frame.columns if "income" in c or "class" == c]
        if not candidates:
            raise ValueError(f"Không tìm thấy cột nhãn income. Các cột hiện có: {list(frame.columns)}")
        frame = frame.rename(columns={candidates[0]: "income"})
    frame["income"] = frame["income"].astype("string").str.strip().str.rstrip(".")

    # Dataset contract checks: stop early if the remote source has changed.
    feature_count = frame.drop(columns=["income"]).shape[1]
    missing_rates = frame.drop(columns=["income"]).isna().mean()
    if len(frame) < 10_000 or feature_count < 10:
        raise ValueError(
            f"Adult dataset không còn đạt ngưỡng đề bài: rows={len(frame)}, features={feature_count}."
        )
    if not (missing_rates >= 0.05).any():
        raise ValueError(
            "Không tìm thấy thuộc tính có missing rate >= 5%. Hãy kiểm tra lại dữ liệu nguồn/marker '?'."
        )
    if frame["income"].isna().any():
        raise ValueError("Cột nhãn income đang có giá trị thiếu; cần kiểm tra nguồn trước khi tiếp tục.")
    return frame


def _image_column(split) -> str:
    """Find the image column in a Hugging Face image split."""
    names = list(split.features.keys())
    for candidate in ("img", "image", "images"):
        if candidate in names:
            return candidate
    for name, feature in split.features.items():
        if feature.__class__.__name__.lower() == "image":
            return name
    raise ValueError(f"Không xác định được cột ảnh. Columns: {names}")


def _split_to_arrays(split) -> tuple[np.ndarray, np.ndarray]:
    """Decode one split to uint8 RGB arrays; memory use is ~3 bytes/pixel."""
    image_col = _image_column(split)
    n = len(split)
    images = np.empty((n, 32, 32, 3), dtype=np.uint8)
    labels = np.empty(n, dtype=np.int64)
    for idx in range(n):
        row = split[idx]
        image = row[image_col]
        if hasattr(image, "convert"):
            image = image.convert("RGB")
        array = np.asarray(image, dtype=np.uint8)
        if array.ndim == 2:
            array = np.repeat(array[..., None], 3, axis=2)
        if array.shape != (32, 32, 3):
            from PIL import Image
            array = np.asarray(Image.fromarray(array).convert("RGB").resize((32, 32)), dtype=np.uint8)
        images[idx] = array
        labels[idx] = int(row["label"])
    return images, labels


def load_cifar10_dataset() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, list[str]]:
    """Load CIFAR-10 train/test from Hugging Face as uint8 NumPy arrays.

    Returns X_train, y_train, X_test, y_test, class_names. No image data is written
    to the Git repository; the Hugging Face cache is kept under data/raw/.hf_cache.
    """
    dataset = _load_hf_dataset(CIFAR10_DATASET_ID)
    if "train" not in dataset or "test" not in dataset:
        raise ValueError(f"CIFAR-10 cần split train/test; nhận được: {list(dataset.keys())}")
    train_split, test_split = dataset["train"], dataset["test"]
    X_train, y_train = _split_to_arrays(train_split)
    X_test, y_test = _split_to_arrays(test_split)

    label_feature = train_split.features.get("label")
    class_names = getattr(label_feature, "names", None)
    if not class_names:
        class_names = ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]
    class_names = list(class_names)

    total = len(X_train) + len(X_test)
    observed_classes = np.unique(np.concatenate([y_train, y_test]))
    if total < 5_000 or len(observed_classes) < 5:
        raise ValueError(
            f"CIFAR-10 không đạt yêu cầu ảnh: total={total}, classes={len(observed_classes)}."
        )
    return X_train, y_train, X_test, y_test, class_names

