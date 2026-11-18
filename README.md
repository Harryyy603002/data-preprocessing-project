# Đồ án Tiền xử lý dữ liệu — Tabular Data + Image Data

> **Trước khi nộp:** thay các trường `[HỌ VÀ TÊN]`, `[MSSV]`, `[LỚP]` bên dưới bằng thông tin thật. Không để placeholder trong bản nộp cuối cùng.

## 1. Thông tin sinh viên

- **Họ và tên:** [HỌ VÀ TÊN]
- **MSSV:** [MSSV]
- **Lớp:** [LỚP]
- **Repository:** https://github.com/Harryyy603002/data-preprocessing-project
- **Học phần:** Tiền xử lý dữ liệu

## 2. Phạm vi đồ án

Đồ án chọn đúng hai nhánh theo đề:

- **Phần (a) — Tabular Data:** Adult Census Income.
- **Phần (b) — Image Data:** CIFAR-10.

Cuốn Jupyter Book có bốn notebook chương (EDA + preprocessing cho từng loại dữ liệu), một trang mở đầu và một chương báo cáo/thảo luận. Những kết quả số, p-value, biểu đồ và kết luận cuối cùng phải được sinh ra bằng cách chạy notebook trên máy của sinh viên; repository ban đầu không chứa số liệu giả lập.

## 3. Nguồn dữ liệu

| Dataset | Nguồn công khai | Quy mô nguồn | Mục đích |
|---|---|---:|---|
| Adult Census Income | [Hugging Face — scikit-learn/adult-census-income](https://huggingface.co/datasets/scikit-learn/adult-census-income) | 32,561 dòng; 14 biến đầu vào + nhãn | EDA thống kê, missing values, imputation, outlier, scaling, encoding, feature selection, imbalance |
| CIFAR-10 | [Hugging Face — uoft-cs/cifar10](https://huggingface.co/datasets/uoft-cs/cifar10) | 50,000 train + 10,000 test; 10 lớp | pHash, pixel distribution, resizing, color space, normalization, augmentation, PCA/t-SNE, edge detection, ablation |

Nguồn Adult hiển thị các giá trị thiếu dưới dạng `?`; bộ tải trong `src/data_loading.py` chuyển dấu này thành `NaN` và kiểm tra lại rằng tối thiểu một thuộc tính có tỷ lệ thiếu từ 5% trở lên. Bộ tải CIFAR-10 xác thực tối thiểu 5.000 ảnh và 5 lớp. Dữ liệu được tải tự động từ Hugging Face ở lần chạy đầu tiên, cache ở `data/raw/.hf_cache` và **không được commit vào repository**.

**Ghi chú giấy phép:** Adult trên trang Hugging Face khai báo CC0-1.0. Trang bản sao CIFAR-10 trên Hugging Face hiện không nêu giấy phép riêng; hãy kiểm tra điều khoản nguồn gốc CIFAR-10 trước khi tái phân phối dữ liệu. Đồ án chỉ tải dữ liệu vào cache cá nhân, không lưu bộ ảnh vào GitHub.

## 4. Cấu trúc repository

```text
data-preprocessing-project/
├── .github/workflows/deploy-book.yml   # tự build và publish GitHub Pages
├── .gitignore
├── README.md
├── UPLOAD_GUIDE.md                     # upload toàn bộ bằng GitHub Web, không cần Git
├── requirements.txt
├── book/
│   ├── _config.yml                     # cấu hình Jupyter Book v1
│   ├── _toc.yml                        # mục lục cuốn book
│   ├── index.md                        # mở đầu và phạm vi
│   ├── 01_EDA_tabular.ipynb            # EDA bảng
│   ├── 02_preprocessing_tabular.ipynb  # preprocessing bảng
│   ├── 04_EDA_image.ipynb              # EDA ảnh
│   ├── 05_preprocessing_image.ipynb    # preprocessing ảnh
│   ├── report.md                       # báo cáo so sánh và thảo luận
│   ├── coverage_checklist.md           # đối chiếu yêu cầu/rubric theo chương
│   └── references.bib                  # tài liệu tham khảo
├── src/
│   ├── __init__.py
│   ├── data_loading.py                 # tải/kiểm tra dữ liệu từ Hugging Face
│   ├── tabular_analysis.py             # tiện ích thống kê và tiền xử lý bảng
│   └── image_analysis.py               # pHash, resize, augmentation, edges
└── data/
    ├── raw/.gitkeep                    # dữ liệu/cache sẽ tự tải, không commit
    └── processed/.gitkeep              # sản phẩm trung gian, không commit
```

## 5. Upload lên GitHub không cần Git

Nếu bạn thao tác thủ công trên website GitHub, làm theo file [UPLOAD_GUIDE.md](UPLOAD_GUIDE.md). Bộ khung chưa yêu cầu cài Git để upload; chỉ cần giải nén ZIP và dùng **Add file → Upload files**.

## 6. Cài đặt môi trường trên Windows 11

Khuyến nghị **Python 3.11 64-bit** và VS Code có extension Python + Jupyter. Không cần cài CUDA, PyTorch hay TensorFlow vì đồ án này dùng các thuật toán thống kê/ML và OpenCV chạy CPU; GPU RTX 2050 không bắt buộc.

Mở thư mục repository đã giải nén bằng VS Code, sau đó mở Terminal trong VS Code và chạy lần lượt:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m ipykernel install --user --name preprocessing-project --display-name "Python (preprocessing-project)"
```

Nếu PowerShell chặn kích hoạt môi trường, có thể dùng terminal **Command Prompt** và chạy:

```bat
.venv\Scripts\activate.bat
```

Trong VS Code, mở một notebook, chọn kernel **Python (preprocessing-project)** hoặc kernel trỏ đến `.venv`, rồi chạy các cell từ đầu đến cuối.

## 7. Chạy đồ án theo đúng thứ tự

1. `book/01_EDA_tabular.ipynb`
2. `book/02_preprocessing_tabular.ipynb`
3. `book/04_EDA_image.ipynb`
4. `book/05_preprocessing_image.ipynb`

Lần chạy đầu cần Internet để tải dữ liệu. Adult khoảng vài MB; CIFAR-10 có khoảng 60.000 ảnh nên tải và giải mã lâu hơn. Laptop 12 GB RAM nên giữ các notebook chạy lần lượt, không mở nhiều kernel cùng lúc. Các bước pHash/PCA/t-SNE và ablation là bước tốn thời gian nhất; notebook đã giới hạn một số phép trực quan hóa theo mẫu có seed cố định và in rõ kích thước mẫu.

**Quan trọng:** sau khi chạy xong từng notebook, nhấn **Save** (`Ctrl+S`) để lưu output/biểu đồ vào file `.ipynb`. Không xóa output trước khi publish book. Nếu notebook báo lỗi, xử lý lỗi trước khi chuyển chương; không bỏ qua cell lỗi rồi coi như đã hoàn tất.

## 8. Build Jupyter Book trên máy

Trong terminal đang ở thư mục repository gốc:

```powershell
jupyter-book --version
jupyter-book build book/
```

Trang web build ra tại `book/_build/html/index.html`. Mở file đó trong trình duyệt để kiểm tra mục lục, biểu đồ, bảng và công thức.

Cấu hình book đặt `execute_notebooks: off` để lần build/publish không tự tải lại 60.000 ảnh hoặc chạy những thí nghiệm nặng. Vì vậy, **cần chạy và lưu output của cả bốn notebook trước khi build cuối cùng**. Workflow GitHub Pages cũng chỉ render notebook đã lưu output; không chạy thí nghiệm trên máy chủ GitHub.

## 9. Xuất bản GitHub Pages

1. Đẩy toàn bộ nội dung repository lên nhánh `main`.
2. Trên GitHub mở **Settings → Pages**.
3. Ở **Build and deployment → Source**, chọn **GitHub Actions**.
4. Mở tab **Actions**; workflow `Build and deploy Jupyter Book` tự chạy sau mỗi lần push lên `main`.
5. Khi workflow có dấu xanh, mở **Settings → Pages** để lấy URL GitHub Pages và kiểm tra trang book.

Đường dẫn dự kiến có dạng:

`https://harryyy603002.github.io/data-preprocessing-project/`

Nếu username/repository thay đổi, URL cũng thay đổi. Chỉ nộp link trang book sau khi workflow thành công và trang web truy cập được.

## 10. Nguyên tắc tái lập và chống rò rỉ dữ liệu

- Dùng random seed 42 cho thao tác lấy mẫu/augmentation/mô hình có ngẫu nhiên.
- Train/test được tách trước khi fit imputer, scaler, encoder và mô hình.
- Target Encoding cross-fit trong train; test chỉ được transform.
- SMOTE/ADASYN/undersampling chỉ áp dụng trên train; test giữ phân phối gốc.
- Augmentation chỉ áp dụng cho train; ablation test dùng ảnh gốc.
- Dữ liệu thô, cache Hugging Face và kết quả trung gian bị loại khỏi Git bởi `.gitignore`.
- Mọi kết luận trong báo cáo phải trích từ output thực tế trong notebook; không chép số minh họa hoặc đoán trước kết quả.

## 11. Giới hạn cần nêu trong báo cáo

- Little’s MCAR được chạy trên ma trận có categorical ordinal-coded để đưa về dạng số; p-value phải được diễn giải thận trọng. Kiểm định này chỉ kiểm tra MCAR, không tự phân biệt MAR với MNAR.
- KS cho tập trước/sau loại ngoại lai là so sánh mô tả trên hai mẫu lồng nhau; không xem p-value như kiểm định độc lập hoàn hảo.
- CIFAR pHash/near-duplicate được rà soát trên mẫu cố định tối đa 5.000 ảnh; pHash bằng nhau chỉ là candidate. Ảnh chỉ tự động loại khi pixel-identical được xác nhận bằng SHA-256 trên toàn bộ train.
- Color-space PCA, t-SNE và edge analysis dùng mẫu có seed để giữ thời gian/RAM hợp lý; ghi rõ kích thước mẫu khi thảo luận.
- CIFAR-10 32×32 nên resize lên 64×64/128×128 là upscale, không tạo chi tiết ảnh mới.
- Với class imbalance, SMOTE/ADASYN được thử trên tập biến số để tránh nội suy giả các mã One-Hot; kết quả chỉ đại diện thí nghiệm numeric-only này.

## 12. Checklist trước khi nộp

Checklist chi tiết đối chiếu đề và rubric nằm ở [book/coverage_checklist.md](book/coverage_checklist.md).

- [ ] Điền họ tên, MSSV và lớp; xóa toàn bộ placeholder.
- [ ] Notebook 1–4 chạy từ đầu đến cuối không có lỗi.
- [ ] Output và hình được lưu trong các notebook.
- [ ] `jupyter-book build book/` chạy thành công.
- [ ] Đã thảo luận kết quả thực tế trong `book/report.md`.
- [ ] Repository không chứa `.venv`, cache, dữ liệu thô hoặc file quá lớn.
- [ ] GitHub Actions deploy thành công; GitHub Pages hiển thị đầy đủ cuốn book.
- [ ] Kiểm tra link book ở chế độ ẩn danh trước khi nộp Moodle.

---

## Tài liệu chính

- Adult Census Income: https://huggingface.co/datasets/scikit-learn/adult-census-income
- CIFAR-10: https://huggingface.co/datasets/uoft-cs/cifar10
- Jupyter Book v1 documentation: https://jupyterbook.org/v1/
- Little (1988), DOI: https://doi.org/10.1080/01621459.1988.10478722
