# Báo cáo Thực hiện (Tuần 3) - OpenAPI Parser & API Inventory

## 1. Mục tiêu
Theo kế hoạch tuần 3, mục tiêu là xây dựng module **OpenAPI Parser** với khả năng:
- Đọc tài liệu OpenAPI định dạng JSON hoặc YAML.
- Hỗ trợ xử lý (resolve) các tham chiếu chéo ($ref) thường dùng trong OpenAPI Specification để tái sử dụng schema.
- Chuẩn hóa dữ liệu đọc được thành mô hình dữ liệu nội bộ (API Inventory) phục vụ cho việc sinh request ở các tuần tiếp theo.

## 2. Kiến trúc và Lựa chọn công nghệ
- **Ngôn ngữ:** Python
- **Thư viện chính:**
  - PyYAML: Xử lý định dạng YAML.
  - jsonref: Tự động phân tích và thay thế các $ref (internal references) trong file OpenAPI thành các dictionary thông thường, giúp tiết kiệm thời gian tự viết hàm đệ quy resolve.
  - pydantic: Dùng để định nghĩa các Data Models (Parameter, Endpoint, APIInventory), giúp đảm bảo kiểu dữ liệu an toàn và dễ dàng trích xuất (serialization).

## 3. Cấu trúc Module đã triển khai
Module được đặt tại src/core/ bao gồm 2 file chính:
- models.py: Định nghĩa các schema của API Inventory.
  - APIInventory: Chứa thông tin tổng quan của API (title, version, servers) và danh sách endpoints.
  - Endpoint: Lưu thông tin của từng route bao gồm path, method, summary, parameters, equest_body, esponses, và security.
  - Parameter: Lưu thông tin tham số truyền vào (header, path, query) và schema của tham số.
- parser.py: Lớp OpenAPIParser.
  - Hàm _load_spec(): Mở file, nạp thành dictionary và dùng jsonref xử lý tham chiếu chéo.
  - Hàm parse(): Trích xuất các route từ node paths và map vào cấu trúc APIInventory.

## 4. Kết quả đạt được
- Khắc phục được khó khăn khi xử lý $ref của OpenAPI.
- Đã hợp nhất (merge) các parameters khai báo chung ở cấp độ path với parameters ở cấp độ method.
- Sẵn sàng cung cấp data model ổn định cho **Baseline Request Generator** ở tuần 4.
