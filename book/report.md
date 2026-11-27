# Báo cáo tổng hợp và thảo luận

> **Cần hoàn thiện sau khi chạy notebook:** điền các giá trị từ output thực tế, chèn kết luận của chính bạn và xóa các dòng hướng dẫn trong ngoặc vuông. Không tạo hoặc suy đoán kết quả thống kê.

## 1. Câu hỏi nghiên cứu

1. Đặc điểm phân phối, tương quan và cơ chế thiếu dữ liệu trong Adult Census Income ảnh hưởng ra sao đến lựa chọn imputation/scaling/encoding?
2. Các detector ngoại lai có phát hiện cùng một nhóm quan sát không? Loại ngoại lai làm thay đổi phân phối như thế nào?
3. Feature selection và resampling thay đổi F1/precision/recall/AUC trên test chưa resample như thế nào?
4. Resize, màu sắc, normalization và augmentation tác động thế nào đến biểu diễn CIFAR-10 và kết quả phân loại?
5. PCA/t-SNE/edge density cung cấp thông tin gì về cấu trúc ảnh và khả năng phân biệt lớp?

## 2. Dữ liệu và tính hợp lệ

### 2.1 Adult Census Income

Nguồn: [Hugging Face — scikit-learn/adult-census-income](https://huggingface.co/datasets/scikit-learn/adult-census-income). Bộ dữ liệu có 32.561 dòng và 14 biến đầu vào; các dấu `?` được chuyển thành `NaN`. Bộ tải tự kiểm tra số dòng, số thuộc tính, có đồng thời biến số/biến phân loại và ít nhất một cột có missing rate ≥ 5%.

**Kết quả thực tế sau khi chạy:**

- Số dòng / số biến đầu vào: [điền từ notebook].
- Các biến có missing rate ≥ 5%: [điền tên cột và tỷ lệ].
- Tỷ lệ nhãn `<=50K` / `>50K`: [điền].

### 2.2 CIFAR-10

Nguồn: [Hugging Face — uoft-cs/cifar10](https://huggingface.co/datasets/uoft-cs/cifar10), thông tin gốc tại [University of Toronto](https://www.cs.toronto.edu/~kriz/cifar.html). Bộ dữ liệu có 50.000 ảnh train và 10.000 ảnh test, kích thước 32×32 RGB, 10 lớp.

**Kết quả thực tế sau khi chạy:**

- Số ảnh train sau loại các bản sao pixel-identical: [điền].
- Số lớp / tỷ số lớp lớn nhất-nhỏ nhất: [điền].
- Số byte-identical duplicate (SHA-256 pixel) được loại: [điền].
- Số nhóm/ảnh pHash trùng hash (candidate, không tự động xóa) và near-duplicate candidate: [điền].

## 3. Kết quả và thảo luận — Tabular Data

### 3.1 EDA, phân phối và tương quan

[Chèn nhận xét dựa trên histogram/KDE và bảng D’Agostino–Pearson. Nêu rõ biến nào lệch chuẩn, không chỉ ghi p-value.]

[Chèn nhận xét heatmap Pearson/Spearman, các cặp có |r| > 0.9 nếu có và hệ quả đa cộng tuyến.]

### 3.2 Missingness và Little’s MCAR

- Little’s MCAR p-value: [điền].
- Quyết định tại alpha=0.05: [bác bỏ / chưa đủ bằng chứng bác bỏ H0].
- Bằng chứng liên hệ missingness với biến quan sát: [nêu cột, p-value, kết luận thận trọng].

**Diễn giải đúng:** Little’s test chỉ đánh giá giả thuyết MCAR. Bác bỏ MCAR không chứng minh MAR; MNAR không thể xác định chỉ bằng các biến quan sát nếu không có thông tin bổ sung. Do biến phân loại được ordinal-code trước khi kiểm định, kết quả cần nêu hạn chế này.

### 3.3 Imputation

| Phương pháp | RMSE MCAR 10% | Nhận xét |
|---|---:|---|
| Mean | [điền] | [điền] |
| Median | [điền] | [điền] |
| Mode | [điền] | [điền] |
| KNN k=3 | [điền] | [điền] |
| KNN k=5 | [điền] | [điền] |
| KNN k=10 | [điền] | [điền] |
| MICE | [điền] | [điền] |

[Giải thích phương pháp tốt nhất trong thử nghiệm này và giới hạn vì RMSE chỉ đánh giá các ô số được che MCAR nhân tạo.]

### 3.4 Outlier, scaling và encoding

[So sánh tỷ lệ outlier và Jaccard. Nêu detector nào bảo thủ/nhạy hơn; không tự động coi mọi điểm bị gắn cờ là lỗi.]

[So sánh KS trước/sau lọc ngoại lai; ghi chú hai mẫu lồng nhau nên p-value là chỉ báo mô tả.]

[So sánh Min-Max, Z-score, Robust, Quantile-uniform/normal dựa trên violin plots và Levene.]

[So sánh số chiều của One-Hot, Ordinal, Target, Binary, Frequency; nêu cách TargetEncoder cross-fit train và fit/transform tránh leakage.]

### 3.5 Feature selection và class imbalance

| Phương pháp | Số đặc trưng | Mean 5-fold CV F1 | Std |
|---|---:|---:|---:|
| ANOVA F-test | [điền] | [điền] | [điền] |
| Chi-square | [điền] | [điền] | [điền] |
| Mutual Information | [điền] | [điền] | [điền] |
| Random Forest importance | [điền] | [điền] | [điền] |
| Gradient Boosting importance | [điền] | [điền] | [điền] |
| RFECV | [điền] | [điền] | [điền] |

[Thảo luận feature importance RF/Gradient Boosting và số đặc trưng RFECV chọn.]

[So sánh baseline, SMOTE, ADASYN và Random Under-sampling trên test nguyên trạng bằng precision, recall, F1-macro, AUC-ROC. Ghi rõ thí nghiệm resampling dùng numeric-only để tránh sinh fractional one-hot values.]

## 4. Kết quả và thảo luận — Image Data

### 4.1 EDA, class imbalance và pHash

[Nhận xét histogram/KDE của R/G/B; lớp có brightness/contrast cao/thấp; tỷ lệ max/min.]

- Nhóm có cùng pHash 64-bit (candidate): [điền].
- Byte-identical pixel groups được xác nhận bằng SHA-256: [điền].
- Gần trùng trong mẫu 5.000 ảnh, Hamming ≤ 3: [điền].
- Ảnh tự động loại (chỉ pixel-identical): [điền].

[Giải thích near-duplicate chỉ là candidate, vì pHash có thể có false positive; không tự ý loại ảnh chưa kiểm tra.]

### 4.2 Resize và color space

| Kích thước | Mean SSIM | Mean PSNR (dB) | Nhận xét |
|---|---:|---:|---|
| 32×32 | [điền] | [điền] | [điền] |
| 64×64 | [điền] | [điền] | [điền] |
| 128×128 | [điền] | [điền] | [điền] |

[Nhấn mạnh SSIM/PSNR đo chất lượng tái tạo sau resize→đưa lại về 32×32. CIFAR-10 gốc đã 32×32, upscale không bổ sung thông tin.]

[So sánh explained variance PCA-50 của RGB/Grayscale/HSV/LAB; kết hợp macro-F1 từ ablation trước khi chọn không gian màu.]

### 4.3 Normalization, augmentation và embedding

[So sánh bốn chuẩn hóa; p-value KS phản ánh khác biệt trên thang pixel, không tự nói chuẩn hóa nào tốt hơn.]

[Thảo luận 6 phép augmentation và t-SNE original/augmented; augmentation chỉ ở train. Nêu phép biến đổi nào hợp lý/không hợp lý đối với ảnh tự nhiên.]

[Thảo luận scree plot PCA, số thành phần đạt 90/95/99% (nếu chưa đạt trong số PC đã tính thì ghi rõ giới hạn, không ngoại suy).]

### 4.4 Edge detection và ablation

[So sánh Sobel/Prewitt/Canny ở hai bộ tham số; báo cáo Edge Density theo lớp và ANOVA p-value. Ý nghĩa thống kê không nhất thiết tương đương ý nghĩa thực tiễn.]

| Representation | Feature dimensions | Accuracy | Macro-F1 |
|---|---:|---:|---:|
| RGB baseline | [điền] | [điền] | [điền] |
| Grayscale | [điền] | [điền] | [điền] |
| HSV | [điền] | [điền] | [điền] |
| LAB | [điền] | [điền] | [điền] |
| Z-score per-channel | [điền] | [điền] | [điền] |
| PCA-50 | [điền] | [điền] | [điền] |
| MinMax [-1,1] | [điền] | [điền] | [điền] |
| Z-score global | [điền] | [điền] | [điền] |
| Z-score per-channel | [điền] | [điền] | [điền] |
| RGB + each augmentation | [điền] | [điền] | [điền] |
| Sobel / Prewitt / Canny edge maps | [điền] | [điền] | [điền] |

[Thảo luận cấu hình tốt nhất trên cùng test split chưa biến đổi; nếu augmentation không cải thiện, giải thích khả năng nguyên nhân. Bảng ablation cần đưa từng biến thể đã chạy từ output notebook, không gộp nếu các kết quả khác nhau.]

## 5. So sánh và lựa chọn pipeline cuối cùng

### 5.1 Pipeline tabular đề xuất

[Chọn các bước dựa trên bằng chứng ở notebook: xử lý missing → scaling/encoding → feature selection → model. Nêu thứ tự và lý do.]

### 5.2 Pipeline image đề xuất

[Chọn kích thước, không gian màu, chuẩn hóa và augmentation có hiệu quả; đảm bảo các phép biến đổi chỉ học từ train.]

## 6. Hạn chế và hướng cải tiến

1. Adult là dữ liệu điều tra dân số Hoa Kỳ năm 1994; kết quả không đại diện cho thu nhập hiện tại hoặc quốc gia khác.
2. Little’s MCAR trên categorical ordinal-coded là xấp xỉ; MNAR không thể chứng minh từ dữ liệu quan sát đơn thuần.
3. Một số bước ảnh dùng mẫu để phù hợp RAM/thời gian; cần báo cáo rõ kích thước mẫu.
4. CIFAR-10 ảnh nhỏ 32×32; upscaling không tạo chi tiết mới.
5. Logistic Regression là baseline đơn giản, không đại diện cho mô hình thị giác chuyên sâu.

## 7. Kết luận

[Viết kết luận 1–3 đoạn: bài học về missingness, outlier, encoding/selection; tác động của xử lý ảnh; trade-off giữa thông tin, hiệu năng và chi phí tính toán. Kết luận phải trích số liệu thật từ notebook.]

## 8. Tài liệu tham khảo

Các tài liệu được trích trong báo cáo: Little (1988) {cite}`little1988mcar`, Wang và cộng sự (2004) {cite}`wang2004ssim`, Krizhevsky (2009) {cite}`krizhevsky2009cifar`.

```{bibliography}
```
