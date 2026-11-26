# Checklist đối chiếu yêu cầu đồ án

Trang này giúp lần ngược từng tiêu chí trong đề đến notebook/chương tương ứng. Đánh dấu hoàn thành sau khi đã **chạy cell, lưu output và tự đọc/giải thích được kết quả**. Việc có code chưa đồng nghĩa đã có kết quả được chấm.

| Yêu cầu | Vị trí chính | Trạng thái sau khi tạo bộ khung |
|---|---|---|
| Adult ≥10.000 dòng, ≥10 thuộc tính, có số + phân loại, missing ≥5% | `01_EDA_tabular.ipynb`; `src/data_loading.py` | Có kiểm tra tự động; cần chạy xác nhận |
| D’Agostino–Pearson / Shapiro theo ngưỡng n | `01_EDA_tabular.ipynb` | Code đã có |
| Pearson + Spearman heatmap và cặp có |r| > 0.9 | `01_EDA_tabular.ipynb` | Code đã có |
| Missingno matrix và Little’s MCAR | `01_EDA_tabular.ipynb`; `src/tabular_analysis.py` | Code đã có; ordinal coding được nêu là hạn chế |
| Nhận xét MCAR/MAR/MNAR | `01_EDA_tabular.ipynb`; `report.md` | Cần diễn giải thận trọng từ bằng chứng |
| Mean/median/mode, KNN 3/5/10, MICE; 10% MCAR; RMSE | `02_preprocessing_tabular.ipynb`; `src/tabular_analysis.py` | Code đã có |
| IQR, Z-score, Isolation Forest .01/.05/.1, LOF 10/20/50, DBSCAN, Jaccard, KS | `02_preprocessing_tabular.ipynb`; `src/tabular_analysis.py` | Code đã có |
| MinMax, Z-score, Robust, Quantile uniform/normal; Levene | `02_preprocessing_tabular.ipynb` | Code đã có |
| One-Hot, Ordinal, Target cross-fit, Binary, Frequency; VIF | `02_preprocessing_tabular.ipynb`; `src/tabular_analysis.py` | Code đã có; cần xác nhận từng encoding |
| ANOVA, Chi-square, MI, RF/GB importance, RFE-CV; 5-fold F1 và đường cong số đặc trưng | `02_preprocessing_tabular.ipynb` | Code đã có |
| PCA, t-SNE, UMAP | `02_preprocessing_tabular.ipynb` | Code đã có; UMAP có fallback |
| Resampling SMOTE/ADASYN/undersampling; test không resample | `02_preprocessing_tabular.ipynb` | Code đã có; chỉ áp dụng trên numeric-only, giải thích giới hạn |
| CIFAR-10 ≥5.000 ảnh, ≥5 lớp | `04_EDA_image.ipynb`; `src/data_loading.py` | Có kiểm tra tự động; cần chạy xác nhận |
| Pixel histogram/KDE theo RGB; imbalance >3x; brightness/contrast boxplot | `04_EDA_image.ipynb` | Code đã có |
| pHash collision/near-duplicate và xác minh exact duplicate | `04_EDA_image.ipynb`; `src/image_analysis.py` | Code đã có; chỉ xóa byte-identical |
| Resize ≥3 kích thước; SSIM/PSNR và đường cong | `05_preprocessing_image.ipynb`; `src/image_analysis.py` | Code đã có |
| RGB/Grayscale/HSV/LAB; PCA-50 explained variance | `05_preprocessing_image.ipynb` | Code đã có |
| 4 normalization + KS test | `05_preprocessing_image.ipynb` | Code đã có |
| ≥5 augmentation + t-SNE original/augmented | `05_preprocessing_image.ipynb` | Code đã có; augmentation chỉ trên train trong ablation |
| PCA scree, 90/95/99%, 2D PCA; t-SNE | `05_preprocessing_image.ipynb` | Code đã có; phải ghi rõ nếu mục tiêu variance chưa đạt trong số PC đã tính |
| Sobel/Prewitt/Canny, ≥2 settings, edge density và ANOVA | `05_preprocessing_image.ipynb`; `src/image_analysis.py` | Code đã có |
| Ablation k-NN/Logistic Regression trước/sau từng nhánh | `05_preprocessing_image.ipynb` | Logistic Regression baseline; cần chạy và phân tích |
| Mỗi kỹ thuật có lý thuyết, code, phân tích | Tất cả notebook và `report.md` | Khung có sẵn; sinh viên phải hoàn thiện nhận xét dựa output |
| README, requirements, Jupyter Book, GitHub Pages | `README.md`, `requirements.txt`, `.github/workflows/deploy-book.yml` | Đã tạo; chưa xác nhận build/deploy thật |

## Điều kiện bắt buộc trước khi nộp

- [ ] Thay tên/MSSV/lớp trong `README.md`, `book/index.md`, `book/_config.yml`.
- [ ] Chạy trọn 4 notebook theo thứ tự trong README, lưu output, không còn cell lỗi.
- [ ] Kiểm tra dataset contract Adult và CIFAR-10 đều pass.
- [ ] Hoàn thiện mọi `[điền]` và `[Chèn...]` trong `book/report.md` bằng kết quả thật.
- [ ] Chạy `jupyter-book build book/` thành công từ thư mục gốc.
- [ ] Đẩy lên GitHub, bật Pages bằng GitHub Actions, kiểm tra URL ở chế độ ẩn danh.
- [ ] Đọc lại và tự giải thích được các phép kiểm định, metric, thuật toán và kết luận khi vấn đáp.

**Lưu ý:** các nhãn “Code đã có” là tình trạng mã nguồn trong bộ khung, không phải cam kết rằng phép thử đã chạy thành công trên máy của bạn. Hãy ghi rõ giới hạn tính toán/mẫu và không tự điền p-value hoặc metric chưa được tạo.
