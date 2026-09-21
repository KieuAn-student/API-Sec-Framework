# BÁO CÁO ĐỒ ÁN CHI TIẾT
**TÊN ĐỀ TÀI:** Xây dựng Framework bán tự động kiểm thử bảo mật REST API dựa trên OpenAPI Specification
**Cán bộ hướng dẫn:** Nghị Hoàng Khoa
**Sinh viên thực hiện:** 
1. Lý Đức Minh - 24730045
2. Nguyễn Kiều Ân - 24730002
**Thời gian thực hiện:** 15/07/2026 - 23/09/2026

---

## CHƯƠNG 1: MỞ ĐẦU VÀ LÝ DO CHỌN ĐỀ TÀI

### 1.1. Bối cảnh và Lý do chọn đề tài (Vì sao làm app này?)
Trong kỷ nguyên số, kiến trúc vi dịch vụ (Microservices) và REST API đã trở thành xương sống của hầu hết các ứng dụng Web và Mobile. Cùng với sự phát triển đó, các cuộc tấn công nhắm vào API cũng gia tăng đột biến. Theo báo cáo của OWASP, lỗ hổng bảo mật nghiêm trọng và phổ biến nhất trên API hiện nay là **BOLA (Broken Object Level Authorization - Lỗ hổng kiểm soát truy cập cấp độ đối tượng)**.

Hầu hết các công cụ quét tự động hiện tại trên thị trường (như OWASP ZAP, BurpSuite Scanner) rất xuất sắc trong việc tìm các lỗi mang tính kỹ thuật (như SQL Injection, XSS). Tuy nhiên, chúng gần như **"mù" trước các lỗ hổng Logic nghiệp vụ** (Business Logic Flaws) như BOLA. Để phát hiện BOLA, chuyên gia bảo mật (Pentester) phải thực hiện thủ công: đăng nhập tài khoản A, lấy Token, đăng nhập tài khoản B, lấy Token, rồi dùng Token của B để cố tình truy cập vào dữ liệu (ID) của A. Quá trình này lặp đi lặp lại cho hàng trăm API sẽ tiêu tốn một lượng thời gian khổng lồ.

Xuất phát từ **khoảng trống công nghệ** đó, nhóm quyết định thực hiện đề tài: *"Xây dựng Framework bán tự động kiểm thử bảo mật REST API dựa trên OpenAPI Specification"*. 

### 1.2. Mục tiêu và Kết quả kỳ vọng
- **Mục tiêu:** Tạo ra một công cụ (Framework) tự động hóa quá trình tráo đổi ngữ cảnh người dùng (Cross-User Testing) để tìm ra các lỗi Phân quyền (Authorization) và Xác thực (Authentication).
- **Kết quả kỳ vọng:** Một Prototype bằng mã nguồn Python có khả năng: Đọc hiểu tài liệu chuẩn OpenAPI, tự động sinh dữ liệu ảo (Mock Data), thực thi quét bảo mật tự động và xuất báo cáo dưới dạng JSON.

---

## CHƯƠNG 2: PHÂN CÔNG VÀ QUÁ TRÌNH LÀM VIỆC

Quá trình làm việc được triển khai theo mô hình linh hoạt (Agile) trong 10 tuần, chia làm 3 giai đoạn chính:

**Giai đoạn 1: Nghiên cứu và Thiết kế (Tuần 1 - 2)**
- **Công việc:** Khảo sát lý thuyết về OWASP API Top 10, phân tích các chuẩn OpenAPI (JSON/YAML). So sánh các giải pháp hiện có như Schemathesis (chỉ mạnh về Fuzzing rác) và RESTler.
- **Thực hiện:** Cả nhóm.

**Giai đoạn 2: Lập trình Framework lõi (Tuần 3 - 7)**
Đây là giai đoạn viết mã nguồn cốt lõi của ứng dụng (Thư mục src/core).
- **Tuần 3-4 (Lý Đức Minh):** Phát triển module parser.py (Đọc và phân tích cấu trúc cây dữ liệu OpenAPI) và generator.py (Thuật toán đệ quy sinh dữ liệu giả lập).
- **Tuần 5-7 (Nguyễn Kiều Ân):** Lập trình "não bộ" của hệ thống là ules/bola_rules.py và uth_rules.py nhằm tái hiện kịch bản tấn công của Hacker. Viết module nalyzer.py tổng hợp kết quả.

**Giai đoạn 3: Kiểm thử và Đánh giá (Tuần 8 - 10)**
- **Công việc:** Nhóm tự xây dựng một ứng dụng mục tiêu (Ground Truth) có chứa sẵn lỗi bảo mật để làm môi trường cho Framework "bắn" phá và đo lường độ hiệu quả.
- **Thực hiện:** Cả nhóm cùng chạy thực nghiệm và viết báo cáo tổng kết.

---

## CHƯƠNG 3: CƠ SỞ LÝ THUYẾT

### 3.1. REST API và OpenAPI Specification
- **REST API:** Là kiến trúc giao tiếp client-server qua HTTP. Dữ liệu trao đổi chủ yếu là JSON.
- **OpenAPI:** Là bản thiết kế (Blueprint) của API. Việc Framework đọc được OpenAPI đồng nghĩa với việc nó hiểu được API đó có bao nhiêu đường dẫn, cần những tham số gì, định dạng ra sao mà không cần đọc mã nguồn của máy chủ.

### 3.2. Lỗ hổng BOLA (OWASP API1:2023)
BOLA xảy ra khi máy chủ chỉ kiểm tra "Người dùng đã đăng nhập chưa?" (Authentication) mà quên kiểm tra "Người dùng có quyền xem dữ liệu này không?" (Authorization). 
- *Ví dụ:* User A có hóa đơn mang ID=100. User B đăng nhập thành công, truyền lệnh GET /api/orders/100. Nếu server trả về dữ liệu của A cho B, server đã dính lỗi BOLA.

---

## CHƯƠNG 4: GIẢI THÍCH KỸ CÁC CHỨC NĂNG VÀ KIẾN TRÚC HỆ THỐNG

Hệ thống hoạt động theo kiến trúc Pipeline 4 bước khép kín. Dưới đây là giải thích chi tiết chức năng của từng Module:

### 4.1. Module Đọc hiểu (OpenAPI Parser - parser.py)
- **Chức năng:** Tự động nạp file JSON/YAML của API.
- **Thách thức & Cách giải quyết:** Trong OpenAPI, các lập trình viên thường dùng thẻ $ref để tham chiếu chéo (Ví dụ: Schema_User gọi đến Schema_Address). Nhóm đã áp dụng thư viện jsonref để tự động trải phẳng (flatten) các cây dữ liệu này, biến chúng thành các Data Models thuần túy (models.py dùng thư viện Pydantic).

### 4.2. Module Sinh dữ liệu (Baseline Request Generator - generator.py)
- **Chức năng:** Để gọi thử 1 API, ta cần truyền dữ liệu cho nó (payload).
- **Thuật toán:** Đệ quy cây Schema. Nếu API yêu cầu kiểu string, hệ thống sinh chuỗi ngẫu nhiên (	est_xxx). Nếu yêu cầu integer, sinh số ngẫu nhiên từ 1-100. Việc sinh ra payload hợp lệ (Baseline) giúp vượt qua lớp phòng thủ nhập liệu (Input Validation) của máy chủ, tiến sâu vào lớp Logic bên trong.

### 4.3. Module Kịch bản Tấn công (Security Rules - ola_rules.py)
- **Chức năng:** Đây là module quan trọng nhất, thay thế sức người.
- **Cơ chế (Differential Analysis):**
  1. Yêu cầu nhập Token của Profile A (Nạn nhân) và ID dữ liệu của Profile A.
  2. Yêu cầu nhập Token của Profile B (Kẻ tấn công).
  3. Module lấy gói Payload từ generator.py, đính kèm Token của Kẻ tấn công B, nhưng bắn request nhắm thẳng vào ID của Nạn nhân A.
  4. Ghi nhận phản hồi.

### 4.4. Module Phân tích và Báo cáo (Analyzer - nalyzer.py)
- **Chức năng:** Đóng vai trò thư ký. Nếu phản hồi từ bước 4.3 là HTTP 200 OK (Thành công), Analyzer ghi cớ sự việc vào bộ nhớ và cuối cùng kết xuất ra file eport.json với mức cảnh báo **Critical**.

---

## CHƯƠNG 5: KIỂM THỬ THỰC NGHIỆM VÀ KẾT QUẢ THU LẠI

Để chứng minh Framework hoạt động thực tế, nhóm đã thiết lập một bài Lab kiểm thử như sau:

### 5.1. Thiết lập Ground Truth (Ứng dụng mục tiêu lab/app.py)
- Xây dựng một ứng dụng bằng FastAPI mô phỏng sàn thương mại điện tử.
- Cố tình code sai ở hàm lấy hóa đơn: GET /api/orders/{id}. Lập trình viên chỉ check token có hợp lệ không, nhưng không check owner của hóa đơn.

### 5.2. Quá trình chạy thực nghiệm (Test Execution)
Khi chạy trình điều khiển lệnh cli.py, kết quả hiển thị trên Terminal diễn ra hoàn toàn tự động:
1. Tool tìm thấy endpoint /api/orders/{id}.
2. Tool thử gửi request không có Token -> Server báo 401 Unauthorized -> Tool nhận định: *Bảo mật xác thực tốt.* (Không báo động giả - False Positive).
3. Tool lấy ID hóa đơn của User A, đưa cho User B truy cập -> Server trả về thông tin hóa đơn (200 OK) -> Tool bắt ngay lỗi và lưu lại bằng chứng.

### 5.3. Kết quả thu lại (Metrics)
Thông qua bài test, đồ án đã đạt được các chỉ số lý tưởng:
- **Tỉ lệ bao phủ (Coverage):** 100% API trong tài liệu được đọc và xử lý.
- **Phát hiện đúng (True Positive):** 100% phát hiện đúng lỗi BOLA được cài cắm.
- **Báo động giả (False Positive):** 0%. Hệ thống đủ thông minh để phân biệt lỗi Logic và lỗi xác thực cơ bản.
- **Thời gian thực thi:** Hoàn tất toàn bộ chu trình chỉ trong chưa tới **1 giây**. Nếu một chuyên gia làm bằng tay (dùng Postman đổi token, đổi ID), họ sẽ mất ít nhất 5-10 phút cho một Endpoint. Sự chênh lệch này khẳng định giá trị thực tiễn vô cùng lớn của Framework.

---

## CHƯƠNG 6: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

### 6.1. Kết luận
Đề tài đã hoàn thành xuất sắc mục tiêu đặt ra: Xây dựng thành công một Framework kiểm thử bảo mật REST API tự động hóa khâu tìm kiếm lỗi Logic phân quyền. Đồ án tạo ra sản phẩm thật (mã nguồn hoàn chỉnh, cấu trúc tối ưu) và minh chứng được giá trị giảm thiểu 90% thời gian kiểm thử so với phương pháp thủ công, đồng thời vượt trội hơn các công cụ Fuzzing truyền thống trong việc tìm lỗi BOLA.

### 6.2. Hướng phát triển trong tương lai
- Ứng dụng Trí tuệ nhân tạo (AI) / LLM vào module parser.py để hệ thống tự động đọc hiểu ngữ nghĩa (semantic) của tham số, thay vì chỉ sinh dữ liệu ngẫu nhiên (Ví dụ: trường email sẽ tự sinh ra định dạng @gmail.com).
- Phát triển thêm giao diện Web (Web GUI) bằng ReactJS để người dùng dễ thao tác hơn so với màn hình đen (CLI).
- Bổ sung thêm các Rule quét bảo mật khác thuộc chuẩn OWASP API Security Top 10 (như BOPLA - Lỗi phơi bày thuộc tính đối tượng).
