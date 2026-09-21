# REST API Security Testing Framework

Đây là Framework kiểm thử bảo mật tự động dành cho REST API, tập trung phát hiện lỗ hổng Phân quyền (BOLA/IDOR) và Xác thực (Authentication) dựa trên OpenAPI Specification. Đồ án được thực hiện nhằm tối ưu hóa thời gian cho chuyên gia bảo mật thay vì phải làm thủ công.

## 1. Hướng dẫn Cài đặt (Installation)

Tải mã nguồn về máy và di chuyển vào thư mục dự án:
`ash
git clone https://github.com/KieuAn-student/API-Sec-Framework.git
cd API-Sec-Framework
`

Cài đặt các thư viện Python cần thiết:
`ash
pip install -r requirements.txt
`

## 2. Hướng dẫn Chạy thử nghiệm (Testing)

Để test công cụ, bạn cần mở 2 cửa sổ Terminal (cmd) để chạy song song:

**Cửa sổ 1: Bật máy chủ mục tiêu (API Lab)**
Khởi động ứng dụng (Ground Truth) có chứa sẵn lỗ hổng bảo mật:
`ash
python -m uvicorn lab.app:app --port 8000
`
*(Hãy để nguyên cửa sổ này chạy ngầm)*

**Cửa sổ 2: Chạy Framework quét bảo mật**
Mở một Terminal khác, chạy trình điều khiển để Framework tự sinh dữ liệu và bắt đầu dò quét:
`ash
python src/cli.py
`

## 3. Xem kết quả (Report)
Sau khi Framework chạy hoàn tất, hệ thống sẽ tự động sinh ra một file báo cáo có tên eport.json tại thư mục gốc. File này sẽ chứa bằng chứng (evidence) chỉ đích danh endpoint bị lỗi và mô tả kịch bản thao túng Token thành công.
