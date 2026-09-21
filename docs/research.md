# Báo cáo Khảo sát (Tuần 1)

## 1. Cơ sở lý thuyết

### 1.1 REST API & OpenAPI Specification
- **REST API**: Là tiêu chuẩn thiết kế API dựa trên kiến trúc REST (Representational State Transfer), sử dụng các phương thức HTTP (GET, POST, PUT, DELETE) và trao đổi dữ liệu thường qua định dạng JSON.
- **OpenAPI Specification (OAS)**: Tiêu chuẩn mô tả REST API, cho phép con người và máy móc hiểu được khả năng của dịch vụ mà không cần truy cập mã nguồn. Phiên bản mới nhất phổ biến là 3.0.x và 3.1.x.

### 1.2 OWASP API Security Top 10 (2023)
Các rủi ro bảo mật API hàng đầu, tập trung vào:
- **API1:2023 - Broken Object Level Authorization (BOLA)**: Lỗ hổng cho phép người dùng thao tác với các đối tượng (objects) của người khác thông qua việc thay đổi ID.
- **API2:2023 - Broken Authentication**: Lỗi xác thực cho phép kẻ tấn công đóng giả người dùng hợp lệ.
- **API3:2023 - Broken Object Property Level Authorization (BOPLA)**: Cho phép kẻ tấn công đọc/ghi các thuộc tính đối tượng không được phép (trước đây là Mass Assignment / Excessive Data Exposure).
- **API5:2023 - Broken Function Level Authorization (BFLA)**: Cho phép người dùng bình thường truy cập các endpoint dành cho admin.

## 2. Các công cụ liên quan
- **Schemathesis**: Công cụ kiểm thử API dựa trên property, sinh dữ liệu tự động để kiểm tra sự tuân thủ (schema compliance). Hữu ích cho việc phát hiện các lỗi crash hoặc sai format, nhưng thiếu bối cảnh bảo mật và kiểm tra authorization phức tạp.
- **RESTler**: Công cụ fuzzing API có trạng thái (stateful) của Microsoft, tự động suy luận thứ tự gọi API (ví dụ: tạo resource rồi mới xóa). Tuy nhiên, RESTler cần nhiều công sức cấu hình từ điển fuzzing và khó phát hiện logic flaws (BOLA).
- **OWASP ZAP API Scan**: Hỗ trợ scan tự động qua file OpenAPI nhưng thiên về các lỗi bảo mật ứng dụng web truyền thống (XSS, SQLi), ít tập trung sâu vào Authorization theo Business logic của API.

## 3. Kết luận và Khoảng trống (Gap)
Các công cụ hiện có đa phần thiếu cơ chế kiểm tra Authorization có bối cảnh (context-aware), vốn cần ít nhất hai profile (người dùng A và người dùng B) để đối chiếu chéo (Differential Analysis). Framework này sẽ tập trung giải quyết khoảng trống đó bằng cơ chế **Multi-profile Testing**.
