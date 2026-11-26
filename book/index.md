# Đồ án Tiền xử lý dữ liệu

**Sinh viên:** Phạm Đặng Thiên Quốc  
**MSSV:** 24127524  
**Lớp:** 24KHMT1  
**Học phần:** Khai Thác Dữ Liệu & Ứng Dụng

## Giới thiệu

Đồ án trình bày quy trình phân tích thống kê khám phá (EDA), thiết kế pipeline tiền xử lý và đánh giá định lượng cho hai loại dữ liệu: **dữ liệu bảng** và **dữ liệu ảnh số**. Mục tiêu không chỉ là làm sạch dữ liệu mà còn giải thích lý do chọn từng kỹ thuật, kiểm soát rò rỉ dữ liệu, so sánh hiệu quả và thảo luận hạn chế.

## Hai bộ dữ liệu

| Phần | Dataset | Quy mô | Bài toán |
|---|---|---:|---|
| (a) Tabular | [Adult Census Income](https://huggingface.co/datasets/scikit-learn/adult-census-income) | 32.561 records; 14 predictors + target | Phân tích hồ sơ và phân loại nhóm thu nhập |
| (b) Image | [CIFAR-10](https://huggingface.co/datasets/uoft-cs/cifar10) | 60.000 ảnh; 10 classes | Phân loại 10 nhóm đối tượng ảnh |

Các hàm tải dữ liệu và kiểm tra điều kiện nằm ở `src/data_loading.py`. Dữ liệu gốc được tải tự động vào Hugging Face cache dưới `data/raw/.hf_cache`; dữ liệu không được đưa vào Git.

## Cấu trúc cuốn book

1. EDA dữ liệu bảng: kiểm định phân phối, tương quan, missingno, Little’s MCAR.
2. Tiền xử lý dữ liệu bảng: imputation, outlier, scaling, encoding, VIF, feature selection, PCA/t-SNE/UMAP và class imbalance.
3. EDA ảnh: pixel histogram/KDE, imbalance, pHash, độ sáng/độ tương phản.
4. Tiền xử lý ảnh: SSIM/PSNR, color spaces, normalization, augmentation, PCA/t-SNE, edge detection và ablation.
5. Báo cáo: so sánh, kết luận và giới hạn.

## Cách đọc kết quả

Các bảng và biểu đồ trong book được sinh bởi notebook. Kết quả có thể khác nếu thay đổi phiên bản thư viện, nguồn dữ liệu hoặc seed. Notebook được thiết kế cho Python 3.11, xử lý trên CPU và giới hạn một số bước nặng bằng mẫu ngẫu nhiên có seed cố định để phù hợp laptop 12 GB RAM.

> **Lưu ý:** các notebook cần được chạy và lưu output trước khi publish. Jupyter Book được cấu hình không tự thực thi notebook khi build để tránh tải dữ liệu và chạy các thí nghiệm nặng trong mỗi lần deploy.
