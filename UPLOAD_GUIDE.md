# Hướng dẫn đưa bộ đồ án lên GitHub bằng trình duyệt

Hướng dẫn này dành cho trường hợp **không cài Git và không dùng terminal để push**.

## A. Giải nén ZIP

1. Tải file ZIP của bộ đồ án.
2. Trong File Explorer, nhấp chuột phải ZIP → **Extract All…**.
3. Mở thư mục `data-preprocessing-project` sau khi giải nén.
4. Kiểm tra bạn nhìn thấy `README.md`, `requirements.txt`, `book`, `src`, `data`, `.github`, `.gitignore`.
5. Không tải dữ liệu vào các thư mục `data/raw` hoặc `data/processed`; các thư mục này chỉ chứa `.gitkeep` ban đầu. Dataset được notebook tự tải khi chạy.

## B. Upload toàn bộ lên repository hiện có

1. Mở https://github.com/Harryyy603002/data-preprocessing-project và chắc chắn đang ở nhánh `main`.
2. Bấm **Add file → Upload files**.
3. Từ File Explorer, kéo thả các mục bên trong thư mục `data-preprocessing-project` vào vùng upload. Hãy kéo cả các thư mục `book`, `src`, `data`, `.github` và các file ẩn dạng `.gitignore` (Windows thường vẫn hiển thị `.gitignore`). Có thể chọn nhiều mục cùng lúc.
4. Đợi danh sách upload hiện đầy đủ đường dẫn. Nếu trình duyệt không nhận thư mục kéo-thả, upload từng thư mục theo từng lượt; mở đúng thư mục đích trên GitHub trước khi bấm **Add file → Upload files**.
5. Kiểm tra `book/`, `src/`, `data/`, `.github/workflows/` giữ đúng cấu trúc. Đảm bảo file cũ `README.md` được thay bằng README mới trong bộ này.
6. Ở phần **Commit changes**, nhập: `Add complete tabular and image preprocessing project`.
7. Chọn commit trực tiếp vào `main` (repository cá nhân hiện không cần tạo pull request) và bấm **Commit changes**.

GitHub hiện giới hạn upload bằng trình duyệt ở 25 MiB cho mỗi file và tối đa 100 file trong một lượt. Các file trong bộ khung này nhỏ hơn giới hạn; không upload file dataset, cache, `.venv` hoặc thư mục `book/_build`. Nếu một file vượt giới hạn, không cố nén dataset vào repo.

## C. Kiểm tra sau upload

- Trang gốc repo phải hiển thị `.github`, `book`, `data`, `src`, `.gitignore`, `README.md`, `requirements.txt`.
- Mở `book/_toc.yml`: có 4 notebook và `report`/`coverage_checklist`.
- Mở tab **Actions** xem workflow `Build and deploy Jupyter Book`.
- Nếu workflow lỗi, mở lần chạy màu đỏ → mở job `build` → xem cell log đầu tiên báo lỗi. Sửa lỗi và upload file đã sửa qua GitHub Web lần nữa.

## D. Thứ tự công việc sau khi upload

1. Tải ZIP repository từ **Code → Download ZIP** hoặc dùng ZIP bộ khung đã giải nén làm thư mục làm việc.
2. Cài Python 3.11 và các thư viện theo README.
3. Chạy 4 notebook và lưu output trong `.ipynb`.
4. Điền `book/report.md` bằng kết quả thật; cập nhật README/metadata sinh viên.
5. Upload lại các file notebook, report, README đã cập nhật bằng GitHub Web, rồi commit.
6. Khi Actions thành công, bật `Settings → Pages → Source: GitHub Actions` nếu chưa bật.

**Quan trọng:** Upload ZIP này chỉ đưa mã nguồn lên GitHub. Các notebook chưa có output được tạo từ bộ dữ liệu thật. Bạn phải chạy và lưu notebook ở VS Code trước khi Pages có biểu đồ/kết quả hoàn chỉnh.
