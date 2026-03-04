# Hệ thống Lưu trữ Key-Value Phân tán (Distributed Key-Value Store)

Dự án này triển khai một hệ thống lưu trữ phân tán dạng Key-Value với khả năng chịu lỗi, đảm bảo tính nhất quán và tự động phục hồi dữ liệu. Hệ thống hoạt động dựa trên mô hình Peer-to-Peer (P2P) với cơ chế đồng thuận Quorum.

## 📌 Các tính năng chính
- **Thao tác cơ bản:** Hỗ trợ đầy đủ `PUT`, `GET`, `DELETE`.
- **Phân vùng dữ liệu:** Sử dụng thuật toán Hash Ring để phân bổ dữ liệu đều trên các Node.
- **Sao lưu (Replication):** Mỗi cặp Key-Value được lưu trữ tại ít nhất 2 Node khác nhau (`REPLICATION_FACTOR = 2`).
- **Tính nhất quán (Quorum):** Sử dụng cơ chế Quorum Read/Write để đảm bảo dữ liệu luôn mới nhất.
- **Phát hiện lỗi:** Cơ chế Heartbeat giúp các Node nhận biết trạng thái sống/chết của nhau trong cụm.
- **Phục hồi (Recovery):** Node mới khởi động lại sẽ tự động lấy Snapshot từ các Node khác để cập nhật dữ liệu thiếu hụt.

## 📂 Cấu trúc mã nguồn
- `node.py`: Thành phần chính xử lý logic lưu trữ và điều phối.
- `client.py`: Giao diện dòng lệnh cho người dùng tương tác với hệ thống.
- `storage.py`: Quản lý lưu trữ dữ liệu tại chỗ (In-memory) và Thread-safe.
- `config.py`: Chứa các thông số cấu hình hệ thống (Nodes, Quorum, Intervals).
- `hash_ring.py`: Thuật toán xác định vị trí lưu trữ của Key.
- `membership.py` & `protocol.py`: Xử lý kết nối, giao thức JSON và Heartbeat.
- `quorum.py` & `replication.py`: Đảm bảo sao lưu và tính nhất quán dữ liệu.
- `recovery.py`: Logic khôi phục dữ liệu qua Snapshot.

## 🚀 Hướng dẫn cài đặt và chạy

### 1. Chuẩn bị
Yêu cầu máy tính đã cài đặt **Python 3.x**. Không cần cài đặt thư viện ngoài (chỉ sử dụng thư viện chuẩn của Python).

### 2. Khởi động các Node
Mở 3 cửa sổ Terminal (hoặc CMD) riêng biệt và chạy các lệnh sau để khởi tạo cụm 3 Node:

```bash
# Terminal 1 (Node 0 - Port 5000)
python node.py 0

# Terminal 2 (Node 1 - Port 5001)
python node.py 1

# Terminal 3 (Node 2 - Port 5002)
python node.py 2