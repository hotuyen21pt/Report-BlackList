import streamlit as st
from PIL import Image
import io
from bson.binary import Binary  # Dùng để lưu dữ liệu file nhị phân vào MongoDB
from models.report_models import Report, Status  
from services.report_service import create_report  # Hàm xử lý lưu báo cáo vào DB
from components.report_form_comp import report_form

def show_create_report_form(user_id):
    """
    Hàm hiển thị form tạo báo cáo blacklist.
    - Cho phép người dùng nhập tiêu đề, mô tả, chọn danh mục.
    - Tải lên hình ảnh/video hoặc nhập link bằng chứng.
    - Khi gửi form, dữ liệu được lưu vào MongoDB qua hàm create_report().
    """

    # Tiêu đề chính của trang
    st.title("Tạo báo cáo Blacklist")

    # Nút hiển thị form (ẩn/hiện)
    if st.button("Tạo báo cáo mới"):
        st.session_state.show_form = True  # Mở form khi nhấn nút

    # Kiểm tra trạng thái form (ẩn/hiện)
    if st.session_state.get("show_form", False):
        # Dùng Streamlit Form để gom các input lại trong một khối gửi duy nhất
        with st.form("create_report_form"):
            # Nhập Thông tin
            title, description, category,detail, status, proof_data, proof_type, proof_link=report_form()
            col1, col2 ,col3= st.columns([3,3,1])
            with col1:
            # Gửi form
                submitted = st.form_submit_button("Xác nhận gửi báo cáo")
            with col3:
                cancel =st.form_submit_button("Hủy")
            if submitted:
                # Kiểm tra bắt buộc: tiêu đề và mô tả phải có
                if not title or not description:
                    st.warning("Vui lòng nhập đầy đủ tiêu đề và mô tả trước khi gửi.")
                    return

                # Tạo đối tượng báo cáo
                report = Report(user_id, title, description, category,detail, proof_data, proof_link=proof_link, proof_type=proof_type)

                # Cập nhật trạng thái báo cáo
                report.status = Status(status)
                
                # Gọi hàm lưu vào MongoDB
                report_id = create_report(report)

                # Thông báo thành công
                st.success(f"Báo cáo đã được lưu thành công! Mã báo cáo: {report_id}")

                # Đóng form và refresh giao diện
                st.session_state.show_form = False
                st.rerun()
            elif cancel:
                st.session_state.show_form = False
                st.info("Đã hủy tạo báo cáo.")
                st.rerun()
