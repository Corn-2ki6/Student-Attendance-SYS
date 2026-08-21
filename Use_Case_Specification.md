# Use Case Specification

---

## 1. Sơ đồ Use-Case

### 1.1. Danh sách các Actor

| STT | Actor | Ý nghĩa |
| :---: | :--- | :--- |
| **1** | Student | Sinh viên, người dùng tham gia lớp học và thực hiện điểm danh. |
| **2** | Lecturer | Giảng viên, người dùng quản lý lớp học và quản lý điểm danh. |

### 1.2. Danh sách các Use-case

| STT | Use-case | Ý nghĩa | Ghi chú (Nhóm) |
| :---: | :--- | :--- | :--- |
| **1** | Login | Đăng nhập hệ thống | Chung |
| **2** | Log out | Đăng xuất hệ thống | Chung |
| **3** | Forgot Password | Khôi phục mật khẩu | Chung |
| **4** | View Profile | Xem thông tin cá nhân | Chung |
| **5** | View Dashboard | Xem bảng điều khiển | Chung |
| **6** | View Classes | Xem danh sách lớp học | Chung |
| **7** | View Schedule | Xem thời khóa biểu | Student |
| **8** | Check Attendance | Thực hiện điểm danh | Student |
| **9** | Enter Attendance Password | Nhập mật khẩu điểm danh | Student |
| **10** | View Attendance History | Xem lịch sử điểm danh | Student |
| **11** | View Attendance Percentage | Xem tỷ lệ điểm danh | Student |
| **12** | View Student List | Xem danh sách sinh viên | Lecturer |
| **13** | Create Attendance Session | Tạo phiên điểm danh | Lecturer |
| **14** | Configure Attendance | Cấu hình điểm danh | Lecturer |
| **15** | Monitor Attendance | Theo dõi điểm danh | Lecturer |
| **16** | Update Attendance | Cập nhật điểm danh | Lecturer |
| **17** | Close Attendance | Đóng phiên điểm danh | Lecturer |
| **18** | View Attendance Report | Xem báo cáo điểm danh | Lecturer |

---

## 2. Use-case Login

### 2.1. Tóm tắt
Use-case này mô tả cách một người dùng (Student/Lecturer) đăng nhập vào Hệ thống điểm danh sinh viên.

### 2.2. Dòng sự kiện
#### 2.2.1. Dòng sự kiện chính
1. Use-case này bắt đầu khi một người dùng muốn đăng nhập vào hệ thống.
2. Hệ thống yêu cầu người dùng nhập tên đăng nhập (email hoặc mã số) và mật khẩu.
3. Người dùng nhập thông tin và yêu cầu đăng nhập.
4. Hệ thống kiểm tra thông tin. Nếu đúng sẽ cho phép người dùng đăng nhập vào hệ thống và chuyển đến trang Dashboard tương ứng với vai trò.

#### 2.2.2. Các dòng sự kiện khác
##### 2.2.2.1. Sai thông tin đăng nhập
Nếu người dùng nhập sai tên đăng nhập hoặc mật khẩu, hệ thống sẽ hiển thị một thông báo lỗi. Người dùng có thể nhập lại hoặc chọn quên mật khẩu.

### 2.3. Các yêu cầu đặc biệt
Không có.

### 2.4. Trạng thái hệ thống trước khi bắt đầu thực hiện Use-case
Người dùng ở trạng thái chưa đăng nhập.

### 2.5. Trạng thái hệ thống sau khi thực hiện Use-case
Nếu thành công, người dùng đã đăng nhập vào hệ thống. Ngược lại, trạng thái không đổi.

### 2.6. Điểm mở rộng
Không có.

---

## 3. Use-case Log out

### 3.1. Tóm tắt
Use-case này cho phép người dùng đăng xuất khỏi hệ thống.

### 3.2. Dòng sự kiện
#### 3.2.1. Dòng sự kiện chính
1. Người dùng chọn chức năng Đăng xuất (Log out).
2. Hệ thống hủy phiên làm việc của người dùng.
3. Hệ thống chuyển hướng người dùng về trang Đăng nhập.

#### 3.2.2. Các dòng sự kiện khác
Không có.

### 3.3. Các yêu cầu đặc biệt
Không có.

### 3.4. Trạng thái hệ thống trước khi bắt đầu thực hiện Use-case
Người dùng đang đăng nhập trong hệ thống.

### 3.5. Trạng thái hệ thống sau khi thực hiện Use-case
Người dùng ở trạng thái chưa đăng nhập (khách).

### 3.6. Điểm mở rộng
Không có.

---

## 4. Use-case Forgot Password

### 4.1. Tóm tắt
Use-case này cho phép người dùng khôi phục lại mật khẩu khi bị quên.

### 4.2. Dòng sự kiện
#### 4.2.1. Dòng sự kiện chính
1. Người dùng chọn chức năng Quên mật khẩu.
2. Hệ thống yêu cầu nhập email liên kết với tài khoản.
3. Người dùng nhập email và xác nhận.
4. Hệ thống kiểm tra email, tạo liên kết đặt lại mật khẩu và gửi vào email đó.
5. Hệ thống thông báo đã gửi email thành công.

#### 4.2.2. Các dòng sự kiện khác
##### 4.2.2.1. Email không tồn tại
Nếu email không có trong hệ thống, hệ thống báo lỗi. Người dùng có thể nhập lại email khác.

### 4.3. Các yêu cầu đặc biệt
Liên kết đặt lại mật khẩu chỉ có hiệu lực trong một khoảng thời gian nhất định (ví dụ 15 phút).

### 4.4. Trạng thái hệ thống trước khi bắt đầu thực hiện Use-case
Người dùng chưa đăng nhập.

### 4.5. Trạng thái hệ thống sau khi thực hiện Use-case
Nếu thành công, email khôi phục được gửi đi. Hệ thống không đổi trạng thái đăng nhập.

### 4.6. Điểm mở rộng
Không có.

---

## 5. Use-case View Profile

### 5.1. Tóm tắt
Use-case này cho phép người dùng xem thông tin cá nhân của mình.

### 5.2. Dòng sự kiện
#### 5.2.1. Dòng sự kiện chính
1. Người dùng chọn chức năng Xem hồ sơ (View Profile).
2. Hệ thống truy xuất thông tin người dùng từ cơ sở dữ liệu.
3. Hệ thống hiển thị các thông tin: Họ tên, Mã số, Email, Khoa/Ngành, v.v.

#### 5.2.2. Các dòng sự kiện khác
Không có.

### 5.3. Các yêu cầu đặc biệt
Không có.

### 5.4. Trạng thái hệ thống trước khi bắt đầu thực hiện Use-case
Người dùng đã đăng nhập.

### 5.5. Trạng thái hệ thống sau khi thực hiện Use-case
Không thay đổi.

### 5.6. Điểm mở rộng
Không có.

---

## 6. Use-case View Dashboard

### 6.1. Tóm tắt
Use-case này cho phép người dùng xem bảng điều khiển tổng quan khi vừa đăng nhập.

### 6.2. Dòng sự kiện
#### 6.2.1. Dòng sự kiện chính
1. Người dùng đăng nhập thành công hoặc bấm vào logo/trang chủ.
2. Hệ thống tổng hợp các thông tin quan trọng:
   - **Với sinh viên:** Lớp học hôm nay, tỷ lệ chuyên cần tổng quan.
   - **Với giảng viên:** Các lớp đang dạy, lịch dạy hôm nay.
3. Hệ thống hiển thị bảng điều khiển.

#### 6.2.2. Các dòng sự kiện khác
Không có.

### 6.3. Các yêu cầu đặc biệt
Không có.

### 6.4. Trạng thái hệ thống trước khi bắt đầu thực hiện Use-case
Người dùng đã đăng nhập.

### 6.5. Trạng thái hệ thống sau khi thực hiện Use-case
Không thay đổi.

### 6.6. Điểm mở rộng
Không có.

---

## 7. Use-case View Classes

### 7.1. Tóm tắt
Use-case này cho phép người dùng xem danh sách các lớp học mà mình tham gia hoặc giảng dạy.

### 7.2. Dòng sự kiện
#### 7.2.1. Dòng sự kiện chính
1. Người dùng chọn chức năng Xem lớp học (View Classes).
2. Hệ thống truy xuất danh sách lớp học liên kết với người dùng.
3. Hệ thống hiển thị danh sách gồm: Mã lớp, Tên môn học, Giảng viên, Học kỳ.

#### 7.2.2. Các dòng sự kiện khác
Không có.

### 7.3. Các yêu cầu đặc biệt
Không có.

### 7.4. Trạng thái hệ thống trước khi bắt đầu thực hiện Use-case
Người dùng đã đăng nhập.

### 7.5. Trạng thái hệ thống sau khi thực hiện Use-case
Không thay đổi.

### 7.6. Điểm mở rộng
Không có.

---

## 8. Use-case View Schedule

### 8.1. Tóm tắt
Use-case này cho phép sinh viên xem thời khóa biểu các môn học trong tuần hoặc tháng.

### 8.2. Dòng sự kiện
#### 8.2.1. Dòng sự kiện chính
1. Sinh viên chọn chức năng Xem thời khóa biểu (View Schedule).
2. Hệ thống lấy dữ liệu lịch học của sinh viên theo thời gian hiện tại.
3. Hệ thống hiển thị lịch học dưới dạng bảng, bao gồm: Môn học, Thời gian, Phòng học.

#### 8.2.2. Các dòng sự kiện khác
Không có.

### 8.3. Các yêu cầu đặc biệt
Không có.

### 8.4. Trạng thái hệ thống trước khi bắt đầu thực hiện Use-case
Sinh viên đã đăng nhập.

### 8.5. Trạng thái hệ thống sau khi thực hiện Use-case
Không thay đổi.

### 8.6. Điểm mở rộng
Không có.

---

## 9. Use-case Check Attendance

### 9.1. Tóm tắt
Use-case này cho phép Sinh viên thực hiện điểm danh để xác nhận sự có mặt trong lớp học.

### 9.2. Dòng sự kiện
#### 9.2.1. Dòng sự kiện chính
1. Sinh viên chọn chức năng điểm danh của một lớp học đang diễn ra.
2. Hệ thống kiểm tra phiên điểm danh có đang mở hay không.
3. Hệ thống hiển thị giao diện điểm danh. Nếu phiên điểm danh có thiết lập mật khẩu, hệ thống sẽ yêu cầu sinh viên nhập mật khẩu.
4. Sinh viên nhập mật khẩu (nếu có) và chọn xác nhận điểm danh.
5. Hệ thống kiểm tra mật khẩu (nếu có). Nếu hợp lệ, hệ thống ghi nhận trạng thái "Có mặt" và thời gian thực hiện.
6. Hệ thống thông báo điểm danh thành công.

#### 9.2.2. Các dòng sự kiện khác
##### 9.2.2.1. Phiên điểm danh chưa mở hoặc đã đóng
Nếu phiên điểm danh chưa được mở hoặc đã hết thời gian, hệ thống hiển thị thông báo lỗi. Use-case kết thúc.

##### 9.2.2.2. Nhập sai mật khẩu điểm danh
Nếu phiên điểm danh có yêu cầu mật khẩu và sinh viên nhập sai, hệ thống báo lỗi và yêu cầu nhập lại mật khẩu.

### 9.3. Các yêu cầu đặc biệt
Không có.

### 9.4. Trạng thái hệ thống trước khi bắt đầu thực hiện Use-case
Sinh viên đã đăng nhập.

### 9.5. Trạng thái hệ thống sau khi thực hiện Use-case
Trạng thái điểm danh của sinh viên được cập nhật vào CSDL.

### 9.6. Điểm mở rộng
Use-case `Enter Attendance Password` (Đã được tích hợp trực tiếp vào Dòng sự kiện chính).

---

## 10. Use-case Enter Attendance Password

### 10.1. Tóm tắt
Use-case này mô tả chi tiết việc sinh viên nhập mật khẩu điểm danh nếu phiên điểm danh có yêu cầu bảo mật.

### 10.2. Dòng sự kiện
#### 10.2.1. Dòng sự kiện chính
1. Tại bước 3 của Use-case Check Attendance, hệ thống phát hiện phiên điểm danh có cài mật khẩu.
2. Hệ thống hiển thị ô nhập mật khẩu.
3. Sinh viên nhập mật khẩu và bấm Xác nhận.
4. Hệ thống kiểm tra khớp mật khẩu và tiếp tục quá trình ghi nhận điểm danh.

#### 10.2.2. Các dòng sự kiện khác
##### 10.2.2.1. Sai mật khẩu
Hệ thống báo mật khẩu không đúng. Sinh viên phải nhập lại.

### 10.3. Các yêu cầu đặc biệt
Không có.

### 10.4. Trạng thái hệ thống trước khi bắt đầu thực hiện Use-case
Sinh viên đang trong quá trình Check Attendance.

### 10.5. Trạng thái hệ thống sau khi thực hiện Use-case
Quay lại hoàn tất Check Attendance nếu đúng mật khẩu.

### 10.6. Điểm mở rộng
Không có.

---

## 11. Use-case View Attendance History

### 11.1. Tóm tắt
Use-case này cho phép sinh viên xem lại chi tiết lịch sử các lần điểm danh của từng môn học.

### 11.2. Dòng sự kiện
#### 11.2.1. Dòng sự kiện chính
1. Sinh viên chọn chức năng Xem lịch sử điểm danh của một môn cụ thể.
2. Hệ thống truy xuất dữ liệu các buổi học đã qua.
3. Hệ thống hiển thị danh sách các buổi học kèm trạng thái: Có mặt, Vắng mặt, Đi trễ.

#### 11.2.2. Các dòng sự kiện khác
Không có.

### 11.3. Các yêu cầu đặc biệt
Không có.

### 11.4. Trạng thái hệ thống trước khi bắt đầu thực hiện Use-case
Sinh viên đã đăng nhập.

### 11.5. Trạng thái hệ thống sau khi thực hiện Use-case
Không thay đổi.

### 11.6. Điểm mở rộng
Không có.

---

## 12. Use-case View Attendance Percentage

### 12.1. Tóm tắt
Use-case này tính toán và hiển thị cho sinh viên thấy tỷ lệ % số buổi đã đi học so với tổng số buổi.

### 12.2. Dòng sự kiện
#### 12.2.1. Dòng sự kiện chính
1. Sinh viên chọn xem thống kê chuyên cần.
2. Hệ thống tính toán: `(Số buổi có mặt / Tổng số buổi đã học) * 100`.
3. Hệ thống hiển thị tỷ lệ % bằng biểu đồ hoặc số liệu.

#### 12.2.2. Các dòng sự kiện khác
Không có.

### 12.3. Các yêu cầu đặc biệt
Nếu tỷ lệ dưới mức quy định (ví dụ dưới 80%), hệ thống có thể bôi đỏ để cảnh báo.

### 12.4. Trạng thái hệ thống trước khi bắt đầu thực hiện Use-case
Sinh viên đã đăng nhập.

### 12.5. Trạng thái hệ thống sau khi thực hiện Use-case
Không thay đổi.

### 12.6. Điểm mở rộng
Không có.

---

## 13. Use-case View Student List

### 13.1. Tóm tắt
Use-case này cho phép giảng viên xem danh sách tất cả sinh viên đăng ký trong một lớp học.

### 13.2. Dòng sự kiện
#### 13.2.1. Dòng sự kiện chính
1. Giảng viên vào một lớp học và chọn Xem danh sách sinh viên.
2. Hệ thống truy xuất dữ liệu danh sách lớp.
3. Hệ thống hiển thị danh sách gồm: MSSV, Họ tên, Trạng thái (đang học, đã rút...).

#### 13.2.2. Các dòng sự kiện khác
Không có.

### 13.3. Các yêu cầu đặc biệt
Không có.

### 13.4. Trạng thái hệ thống trước khi bắt đầu thực hiện Use-case
Giảng viên đã đăng nhập.

### 13.5. Trạng thái hệ thống sau khi thực hiện Use-case
Không thay đổi.

### 13.6. Điểm mở rộng
Không có.

---

## 14. Use-case Create Attendance Session

### 14.1. Tóm tắt
Use-case này cho phép Giảng viên tạo và mở một phiên điểm danh cho sinh viên.

### 14.2. Dòng sự kiện
#### 14.2.1. Dòng sự kiện chính
1. Giảng viên chọn chức năng tạo phiên điểm danh cho một lớp học.
2. Hệ thống yêu cầu nhập cấu hình (thời gian bắt đầu, kết thúc, có dùng mật khẩu không).
3. Giảng viên nhập thông tin và yêu cầu tạo.
4. Hệ thống mở phiên điểm danh và thông báo thành công.

#### 14.2.2. Các dòng sự kiện khác
##### 14.2.2.1. Lỗi cấu hình
Nếu thời gian kết thúc nhỏ hơn thời gian bắt đầu, hệ thống báo lỗi.

### 14.3. Các yêu cầu đặc biệt
Không có.

### 14.4. Trạng thái hệ thống trước khi bắt đầu thực hiện Use-case
Giảng viên đã đăng nhập.

### 14.5. Trạng thái hệ thống sau khi thực hiện Use-case
Phiên điểm danh mới được tạo.

### 14.6. Điểm mở rộng
Không có.

---

## 15. Use-case Configure Attendance

### 15.1. Tóm tắt
Use-case này cho phép giảng viên chỉnh sửa các thông số của một phiên điểm danh đang mở hoặc sắp mở.

### 15.2. Dòng sự kiện
#### 15.2.1. Dòng sự kiện chính
1. Giảng viên chọn một phiên điểm danh và chọn Cấu hình.
2. Hệ thống hiển thị các thông số hiện tại (thời gian, mật khẩu).
3. Giảng viên thay đổi thông số (ví dụ: gia hạn thêm 5 phút) và lưu lại.
4. Hệ thống cập nhật cấu hình và thông báo thành công.

#### 15.2.2. Các dòng sự kiện khác
Không có.

### 15.3. Các yêu cầu đặc biệt
Không có.

### 15.4. Trạng thái hệ thống trước khi bắt đầu thực hiện Use-case
Giảng viên đã đăng nhập và quản lý lớp học.

### 15.5. Trạng thái hệ thống sau khi thực hiện Use-case
Thông tin phiên điểm danh được cập nhật.

### 15.6. Điểm mở rộng
Không có.

---

## 16. Use-case Monitor Attendance

### 16.1. Tóm tắt
Use-case này cho phép giảng viên theo dõi trực tiếp số lượng và danh sách sinh viên đã điểm danh trong lúc phiên điểm danh đang mở.

### 16.2. Dòng sự kiện
#### 16.2.1. Dòng sự kiện chính
1. Giảng viên mở giao diện Theo dõi điểm danh của một phiên đang diễn ra.
2. Hệ thống liên tục cập nhật danh sách sinh viên đã bấm "Xác nhận".
3. Hệ thống hiển thị sĩ số hiện tại: Số sinh viên đã điểm danh / Tổng số sinh viên.

#### 16.2.2. Các dòng sự kiện khác
Không có.

### 16.3. Các yêu cầu đặc biệt
Hệ thống cập nhật danh sách điểm danh khi các dữ liệu điểm danh mới được gửi.

### 16.4. Trạng thái hệ thống trước khi bắt đầu thực hiện Use-case
Giảng viên đã đăng nhập, phiên điểm danh đang mở.

### 16.5. Trạng thái hệ thống sau khi thực hiện Use-case
Không thay đổi.

### 16.6. Điểm mở rộng
Không có.

---

## 17. Use-case Update Attendance

### 17.1. Tóm tắt
Use-case này cho phép giảng viên chỉnh sửa thủ công trạng thái điểm danh của sinh viên (chuyển từ vắng mặt sang có mặt, đi trễ...).

### 17.2. Dòng sự kiện
#### 17.2.1. Dòng sự kiện chính
1. Giảng viên chọn danh sách điểm danh của một buổi học.
2. Giảng viên tìm sinh viên cần sửa và đổi trạng thái (VD: từ Vắng thành Có mặt).
3. Giảng viên bấm Lưu.
4. Hệ thống cập nhật lại trạng thái vào CSDL và thông báo thành công.

#### 17.2.2. Các dòng sự kiện khác
Không có.

### 17.3. Các yêu cầu đặc biệt
Hệ thống có thể lưu lại log (nhật ký) giảng viên đã chỉnh sửa điểm danh lúc nào để tiện kiểm tra.

### 17.4. Trạng thái hệ thống trước khi bắt đầu thực hiện Use-case
Giảng viên đã đăng nhập.

### 17.5. Trạng thái hệ thống sau khi thực hiện Use-case
Trạng thái điểm danh của sinh viên bị thay đổi trong hệ thống.

### 17.6. Điểm mở rộng
Không có.

---

## 18. Use-case Close Attendance

### 18.1. Tóm tắt
Use-case này cho phép giảng viên chủ động đóng phiên điểm danh trước khi hết hạn thời gian đã cài đặt.

### 18.2. Dòng sự kiện
#### 18.2.1. Dòng sự kiện chính
1. Giảng viên chọn phiên điểm danh đang mở và bấm nút Đóng.
2. Hệ thống yêu cầu xác nhận.
3. Giảng viên xác nhận đóng.
4. Hệ thống thay đổi trạng thái phiên thành "Đã đóng", sinh viên không thể điểm danh được nữa.

#### 18.2.2. Các dòng sự kiện khác
Không có.

### 18.3. Các yêu cầu đặc biệt
Tất cả các sinh viên chưa kịp điểm danh lúc này sẽ bị hệ thống tự động gán trạng thái "Vắng mặt".

### 18.4. Trạng thái hệ thống trước khi bắt đầu thực hiện Use-case
Phiên điểm danh đang ở trạng thái Mở.

### 18.5. Trạng thái hệ thống sau khi thực hiện Use-case
Phiên điểm danh chuyển sang trạng thái Đóng.

### 18.6. Điểm mở rộng
Không có.

---

## 19. Use-case View Attendance Report

### 19.1. Tóm tắt
Use-case này cho phép giảng viên xem báo cáo và thống kê chuyên cần tổng quát của cả lớp học.

### 19.2. Dòng sự kiện
#### 19.2.1. Dòng sự kiện chính
1. Giảng viên chọn chức năng Xem báo cáo điểm danh của một lớp học.
2. Hệ thống tổng hợp dữ liệu tất cả các buổi học.
3. Hệ thống hiển thị danh sách sinh viên kèm theo số buổi vắng, số buổi có mặt và tỷ lệ %. Giảng viên có thể chọn Xuất file (Excel/PDF).

#### 19.2.2. Các dòng sự kiện khác
Không có.

### 19.3. Các yêu cầu đặc biệt
Không có.

### 19.4. Trạng thái hệ thống trước khi bắt đầu thực hiện Use-case
Giảng viên đã đăng nhập.

### 19.5. Trạng thái hệ thống sau khi thực hiện Use-case
Không thay đổi.

### 19.6. Điểm mở rộng
Không có.
