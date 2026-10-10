# Bybit Rule — Mô hình giám sát và phát hiện tấn công

## 1. Giới thiệu

Dự án xây dựng mô hình giám sát an toàn thông tin mô phỏng,
hướng đến việc phát hiện các dấu hiệu bất thường liên quan
đến ba kịch bản được phân tích trong sự cố Bybit năm 2025.

Mô hình sử dụng log JSONL, quy tắc YAML theo cấu trúc gần
Sigma, bộ phát hiện do dự án xây dựng và dashboard trực quan.

Dữ liệu thử nghiệm là dữ liệu mô phỏng, không phải log nội bộ
của Bybit. Hệ thống không kết nối hạ tầng Bybit hoặc SIEM
sản xuất.

## 2. Chức năng

- Đọc dữ liệu log JSONL.
- Chuẩn hóa các trường dữ liệu.
- Nạp và thực thi ba quy tắc phát hiện YAML.
- Tạo và lưu cảnh báo.
- Tính TP, FP, FN, TN, Precision, Recall, Accuracy và F1-score.
- Hiển thị kết quả trên dashboard Streamlit.
- Kiểm thử các chức năng chính bằng unittest.

## 3. Ba kịch bản phát hiện

### Kịch bản 1
Phát hiện triển khai phần mềm không được phê duyệt hoặc
sai lệch tính toàn vẹn.

### Kịch bản 2
Phát hiện sai lệch giữa nội dung giao dịch được xác minh
và nội dung giao dịch thực tế được yêu cầu ký.

### Kịch bản 3
Phát hiện giao dịch đến địa chỉ chưa được phê duyệt,
giao dịch vượt ngưỡng giá trị mô phỏng hoặc thay đổi
implementation.

## 4. Cấu trúc thư mục

- `data/`: dữ liệu log mô phỏng.
- `rules/`: các quy tắc phát hiện YAML.
- `src/`: các module xử lý dữ liệu, phát hiện và đánh giá.
- `output/`: kết quả cảnh báo và đánh giá.
- `tests/`: kiểm thử tự động.
- `app.py`: dashboard giám sát.

## 5. Cài đặt

Yêu cầu Python 3.10 trở lên.

Tại thư mục gốc dự án, chạy:

    python -m venv .venv

Trên Windows:

    .venv\Scripts\activate

Cài đặt thư viện:

    pip install -r requirements.txt

## 6. Chạy chương trình

Chạy bộ phát hiện:

    python -m src.main

Mở dashboard:

    streamlit run app.py

Chạy kiểm thử:

    python -m unittest discover -s tests -v

## 7. Giới hạn

Các quy tắc YAML sử dụng schema mô phỏng và chỉ được
thực thi bởi bộ xử lý cú pháp con do dự án xây dựng.
Đây chưa phải parser Sigma đầy đủ hoặc hệ thống SIEM
hoàn chỉnh.

Ngưỡng giao dịch và các trường log được sử dụng nhằm
minh họa nguyên tắc phát hiện. Khi triển khai thực tế,
cần hiệu chỉnh theo tài sản, nghiệp vụ, nguồn log và
mức độ rủi ro của hệ thống.