# Thiết kế Kiến trúc (Tuần 2)

## 1. Yêu cầu Hệ thống
- **Input**: Tài liệu OpenAPI Specification (JSON/YAML) phiên bản 3.0.x / 3.1.x, thông tin xác thực của nhiều người dùng (Profiles).
- **Output**: Báo cáo HTML/JSON chi tiết về các lỗ hổng tìm thấy, mức độ nghiêm trọng (Confidence Score), kèm theo request/response bằng chứng.
- **Tính năng chính**:
  - Tự động parse và chuẩn hóa endpoint.
  - Sinh baseline request với dữ liệu hợp lệ (từ example, schema).
  - Tự động thực hiện các phép biến đổi (Mutation) để kiểm thử Input Validation.
  - Hỗ trợ kiểm thử BOLA, BFLA, BOPLA dựa trên kỹ thuật **Differential Response Analysis** (so sánh phản hồi giữa các người dùng với các quyền khác nhau).

## 2. Kiến trúc Module (Architecture)

Framework bao gồm 5 Module chính:

1. **OpenAPI Parser & API Inventory**:
   - Đọc, giải quyết các tham chiếu (resolve \$ref\), và trích xuất thông tin Endpoint (URL, Method, Parameters, Body Schema, Security Schemes).
   - Lưu trữ dữ liệu vào cấu trúc nội bộ (API Inventory).

2. **Baseline Request Generator**:
   - Dựa vào Schema để sinh dữ liệu ngẫu nhiên hoặc dùng \example\, \default\ được khai báo.
   - Trả ra một mẫu HTTP Request hoàn chỉnh có thể thành công.

3. **HTTP Execution Engine**:
   - Chịu trách nhiệm thực thi các Request.
   - Xử lý Rate Limit, Timeout, Retry logic, và gắn Authentication headers tự động.

4. **Security Test Rules Engine**:
   - **Schema/Input Rule**: Loại bỏ required field, sai data type, vượt quá string length.
   - **Authentication Rule**: Gửi request không có token hoặc token sai/hết hạn.
   - **Authorization Rule (BOLA, BFLA)**: Sinh request từ Profile A (chủ sở hữu object) nhưng dùng token của Profile B (kẻ tấn công).

5. **Response Analyzer & Finding Manager**:
   - So sánh Status Code, Body schema và độ lệch dữ liệu.
   - Phát hiện các bất thường (VD: kỳ vọng 403 Forbidden nhưng trả về 200 OK với dữ liệu nhạy cảm).
   - Loại bỏ trùng lặp (Deduplication) và xuất báo cáo.

## 3. Mô hình Dữ liệu (Data Model)
- **EndpointModel**: \path\, \method\, \parameters\, \equest_schema\, \esponses_schema\, \security\.
- **RequestModel**: \url\, \headers\, \query_params\, \ody\.
- **ResponseModel**: \status_code\, \headers\, \ody\.
- **FindingModel**: \ulnerability_type\, \endpoint\, \severity\, \evidence_request\, \evidence_response\.
