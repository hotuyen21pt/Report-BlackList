import streamlit as st
from db.connection import users_col
from werkzeug.security import check_password_hash

def login_page():
    """Trang đăng nhập đơn giản sử dụng session_state"""
    
    st.title("Đăng nhập")
    username = st.text_input("Tên đăng nhập")
    password = st.text_input("Mật khẩu", type="password")

    if st.button("Đăng nhập"):
        user = users_col.find_one({"username": username})
        if user and check_password_hash(user["password"], password):
            st.session_state.user_id = username
            st.rerun()
        else:
            st.error("Sai tên đăng nhập hoặc mật khẩu.")

    st.markdown("---")
    if st.button("Chưa có tài khoản? Đăng ký ngay"):
        st.session_state.page = "register"
