#***User Story: Đăng báo cáo Blacklist công khai***#

**As a user:** I want to create and publish a blacklist report publicly  
So that I can share verified scam or suspicious cases with the community,and other users can vote Whitelist or Blacklist the report.Reports with more Blacklist votes than Whitelist after 30 days should automatically appear on the Blacklist page.

**Purpose:**

Tính năng giúp người dùng nhanh chóng chia sẻ các trường hợp lừa đảo, tăng độ tin cậy của nền tảng và hỗ trợ phát hiện hành vi xấu.

Hỗ trợ cộng đồng đánh gía tính xác thực của báo cáo thông qua cơ chế vote.

Các báo cáo có nhiều Blacklist sẽ được tự động đưua vào trang Blacklist sau 30 ngày.


**Precondition:**

- Người dùng đã đăng nhập vào hệ thống.
  
- Tài khoản người dùng không bị khóa hoặc giới hạn quyền.

**Feature Flow:**

1.Create a report:

- Người dùng có thể nhấn nút “Tạo báo cáo” trên giao diện chính.
  
- Hệ thống mở form để người dùng nhập thông tin vụ việc cần báo cáo.

2.Choose a Category:

- Người dùng phải chọn ít nhất một danh mục trong số các loại sau:
  
  - Phone Number: Báo cáo số điện thoại lừa đảo, spam…
    
  - Personnel / KOL: Báo cáo cá nhân hoặc người có ảnh hưởng.
      
  - Company: Báo cáo công ty hoặc tổ chức có hành vi gian lận.
     
  - Event: Báo cáo sự kiện hoặc chiến dịch có dấu hiệu bất thường.
     
- Hệ thống lưu danh mục này kèm theo báo cáo.

3.Edit the report:

- Người dùng có thể nhập mô tả chi tiết (Description): lý do đưa vào blacklist, thông tin vụ việc.
  
- Người dùng có thể tải lên bằng chứng (Proof): hình ảnh, video, link hoặc file.
  
- Hệ thống hiển thị xem trước nội dung và yêu cầu xác nhận trước khi lưu.

4.Save as Draft or Publish:

- Người dùng có thể chọn “Save as Draft” để lưu tạm thời (báo cáo không hiển thị công khai).
  
- Người dùng có thể chọn “Publish” để đăng công khai báo cáo lên trang cộng đồng.
  
- Sau khi đăng, hệ thống hiển thị thông báo: “Báo cáo của bạn đã được đăng thành công.”

5.Vote on Report:

- Người dùng khác có thể xem báo cáo công khai.
  
- Người dùng có thể vote Whitelist hoặc vote Blacklist

- Hệ thống lưu số lượt vote và hiển thị tổng số vote trên báo cáo.
  
- Hệ thống cập nhật tổng số vote theo thời gian thực.
  
- Tùy chọn: Báo cáo có thể được sắp xếp theo độ uy tín/điểm vote (Whitelist/Blacklist)

6.Auto-classification after 30 days:

- Sau 30 ngày, hệ thống kiểm tra vote:

- Nếu Blacklist>Whitelist->Tự động đưa báo cáo vào trang Blacklist

- Nếu Whitelist>=Blacklist->Không đưa vào Blacklist, vẫn hiển thị trên trang báo cáo công khai.

- Người dùng được thông báo về trạng thái của báo cáo.

**Acceptance Criteria:**

#1:

- Given: Người dùng đăng nhập và truy cập trang chính.

- When: Nhấn nút “Tạo báo cáo” và nhập đầy đủ thông tin.

- Then: Hiển thị thông báo “Báo cáo cảu bạn đã được đăng thành công”.

#2:

- Given: Người dùng chưa chọn danh mục.

- When: Nhấn “Publish”

- Then: Hệ thống hiển thị cảnh báo “Vui lòng chọn ít nhất một danh mục”

#3

- Given: Người dùng chọn “Save as Draft” 

- When: Báo cáo được lưu tạm thời.

- Then: Hệ thống hiển thị thông báo “Báo cáo đã được lưu nháp”

#4 Vote trên báo cáo: 

- Given: Người dùng khác truy cập vào báo cáo công khai

- When: Người dùng nhấn Whitelist/Blacklist

- Then: Số lượt vote được cập nhật ngay trên báo cáo, tổng số vote hiển thị chính xác.

#5 Auto-classification after 30 days:

- Given: Báo cáo đã được đăng công khai ít nhất 30 ngày

- When: Số Blacklist>Whitelist

- Then: Báo cáo được đưua vào trang Blacklist tự động.

**Postcondition:**

- Báo cáo được lưu vào cơ sở dữ liệu kèm trạng thái (Draft hoặc Published).
  
- Thông tin hiển thị trên trang cộng đồng cùng tổng số vote nếu trạng thái là Published.
  
- Các báo cáo Blacklisted hiển thị trên trang Blacklist.

**Error Handling & Edges Cases:**

- Nếu không nhập mô tả -> nút Publish bị khóa

- Nếu upload file sai định dạng ->Hiển thị “Định dạng không hợp lệ”

- Nếu mất mạng khi lưu ->Hiển thị “Kết nối bị gián đoạn”.

- Người dùng rời trang khi chưa lưu-> Hiển thị cảnh báo “Báo cáo chưa được lưu, bạn có chắc muốn thoát không?”

- Upload tệp quá lớn->Hiển thị cảnh báo “Kích thước tệp vượt quá giới hạn cho phép”

- Người dùng vote nhiều lần->hệ thống chỉ tính một vote trên mỗi báo cáo/người dùng.
