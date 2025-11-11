import streamlit as st
from components import create_report_comp, show_public_reports_comp, edit_report_comp,auto_form
from pages.login.login_page import login_page
from pages.blacklist_page import show_blacklist_page  
from pages.login.login_page import login_page
from pages.login.register_page import register_page

def main():
    """Ứng dụng chính cho hệ thống báo cáo Blacklist"""
    st.set_page_config(page_title="Blacklist Report System", layout="wide")

    # -----------------------------
    # Khởi tạo session state
    # -----------------------------
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "page" not in st.session_state:
        st.session_state.page = "login"

    # -----------------------------
    # Nếu người dùng đã đăng nhập
    # -----------------------------
    if st.session_state.user_id:
        st.sidebar.title(" Menu")
        menu = ["Trang chủ", "Blacklist"]
        choice = st.sidebar.radio("Điều hướng", menu)

        st.sidebar.write(f" Người dùng: `{st.session_state.user_id}`")

        if st.sidebar.button(" Đăng xuất"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

        # -----------------------------
        # Trang chủ với 4 tab
        # -----------------------------
        if choice == "Trang chủ":
            tab1, tab2, tab3, tab4 = st.tabs([
                " Tạo báo cáo thủ công",
                " Tạo báo cáo tự động",
                " Báo cáo công khai",
                " Chỉnh sửa báo cáo của tôi"
            ])

            with tab1:
                create_report_comp.show_create_report_form(st.session_state.user_id)

            with tab2:
                auto_form.show_auto_report_form(st.session_state.user_id)

            with tab3:
                show_public_reports_comp.show_public_reports(st.session_state.user_id)

            with tab4:
                edit_report_comp.edit_my_reports(st.session_state.user_id)

        # -----------------------------
        # Trang Blacklist
        # -----------------------------
        elif choice == "Blacklist":
            show_blacklist_page()

    # -----------------------------
    # Nếu chưa đăng nhập
    # -----------------------------
    else:
        if st.session_state.page == "login":
            login_page()
        elif st.session_state.page == "register":
            register_page()


if __name__ == "__main__":
    main()