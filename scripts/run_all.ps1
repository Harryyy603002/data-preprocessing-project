$notebooks = "01_EDA_tabular","02_preprocessing_tabular","04_EDA_image","05_preprocessing_image"
foreach ($n in $notebooks) {
    jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=-1 "book/$n.ipynb"
    if ($LASTEXITCODE -ne 0) { throw "Lỗi ở notebook $n" }
}
