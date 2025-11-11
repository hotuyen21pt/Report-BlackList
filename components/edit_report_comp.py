import streamlit as st
from utils.functions import edit_report, delete_report  # Thêm hàm delete_report
from db.connection import reports_col
from components.report_form_comp import report_form

def edit_my_reports(user_id):
    """
    Hiển thị danh sách các báo cáo của người dùng hiện tại.
    Cho phép chỉnh sửa hoặc xóa báo cáo.
    """

    st.header(" Quản lý báo cáo của bạn")

    # Lấy danh sách báo cáo của user
    my_reports = list(reports_col.find({"user_id": user_id, "deleted": {"$ne": True}}))

    if not my_reports:
        st.info("Bạn chưa có báo cáo nào.")
        return

    # Duyệt từng báo cáo
    for report in my_reports:
        st.subheader(report["title"])

        # Khóa form riêng cho từng báo cáo
        show_form_key = f"show_form_{report['report_id']}"
        if show_form_key not in st.session_state:
            st.session_state[show_form_key] = False

        col1, col2 = st.columns([1, 1])
        with col1:
            edit_key = f"edit_{report['report_id']}"
            if st.button(" Edit", key=edit_key):
                st.session_state[show_form_key] = True

        with col2:
            delete_key = f"delete_{report['report_id']}"
            if st.button(" Xóa", key=delete_key):
                # Xác nhận trước khi xóa
                confirm_key = f"confirm_delete_{report['report_id']}"
                st.session_state[confirm_key] = True

        # Nếu người dùng vừa nhấn "Xóa"
        confirm_key = f"confirm_delete_{report['report_id']}"
        if st.session_state.get(confirm_key, False):
            st.warning(f" Bạn có chắc muốn xóa báo cáo: '{report['title']}'?")
            c1, c2 = st.columns(2)
            with c1:
                if st.button(" Xác nhận", key=f"confirm_yes_{report['report_id']}"):
                    ok, msg = delete_report(reports_col, report["report_id"], user_id)
                    if ok:
                        st.success(msg)
                        st.session_state.pop(confirm_key, None)
                        st.rerun()
                    else:
                        st.error(msg)
            with c2:
                if st.button(" Hủy", key=f"confirm_no_{report['report_id']}"):
                    st.session_state.pop(confirm_key, None)
                    st.rerun()

        # Nếu form chỉnh sửa đang được mở
        if st.session_state[show_form_key]:
            with st.form(f"edit_form_{report['report_id']}"):
                # Hiển thị form với dữ liệu cũ
                title, description, category, detail, status, proof_data, proof_type, proof_link = report_form(existing=report)

                # Nút submit
                col1,col2=st.columns(2)
                with col1:
                    draft_btn=st.form_submit_button("Save as Draft",key="btn_draft")
                with col2:
                    publish_btn=st.form_submit_button("Publish",key="btn_publish")     
                if draft_btn or publish_btn:
                    status="Draft" if draft_btn else "Publish" 
                    success, msg = edit_report(
                        reports_col,
                        report["report_id"],
                        user_id,
                        title,
                        description,
                        category,
                        detail,
                        status,
                        proof_data,
                        proof_type,
                        proof_link
                    )
                    if success:
                        st.success(msg)
                        st.session_state[show_form_key] = False
                        st.rerun()
                    else:
                        st.error(msg)
