# Ứng Dụng Sắp Xếp Ngoại (External Merge Sort)

Đây là ứng dụng mô phỏng thuật toán Sắp xếp ngoại (External Merge Sort) dành cho các tập tin nhị phân có kích thước lớn, vượt quá dung lượng bộ nhớ chính (RAM). Ứng dụng được viết bằng Python với giao diện đồ họa (GUI).

## Tính năng chính
- **Xử lý tập tin nhị phân:** Đọc và ghi dữ liệu dạng số thực 8-bytes.
- **Mô phỏng giới hạn RAM:** Minh họa quá trình chia nhỏ tệp dữ liệu lớn.
- **Trộn K-Way hiệu quả:** Sử dụng cấu trúc dữ liệu `Min-Heap` để tối ưu hóa quá trình trộn (Merge) các file tạm (Runs).
- **Trực quan hóa (Visualization):** Tự động ghi log chi tiết từng bước nạp dữ liệu vào Buffer và xuất ra đĩa, hiển thị trực tiếp trên giao diện.
- **Công cụ Test:** Tích hợp tính năng sinh bộ dữ liệu nhị phân ngẫu nhiên (15, 50, 100 hoặc tùy chỉnh số lượng) và tính năng xem nội dung file nhị phân.

## Cấu trúc mã nguồn
Dự án được thiết kế theo mô hình phân tách chức năng:
- `main.py`: Chứa giao diện đồ họa (Tkinter) và là điểm khởi chạy.
- `external_sort.py`: Chứa lõi thuật toán bao gồm 2 giai đoạn (Chia Runs và Trộn bằng Min-Heap).
- `utils.py`: Chứa các hàm hỗ trợ thao tác I/O với file nhị phân và sinh dữ liệu mẫu.

## Hướng dẫn sử dụng
1. Clone repository này về máy.
2. Mở Terminal/Command Prompt tại thư mục chứa mã nguồn.
3. Khởi chạy ứng dụng bằng lệnh:
   python main.py
