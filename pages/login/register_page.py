import streamlit as st
from db.connection import users_col
from werkzeug.security import generate_password_hash
from datetime import datetime

def register_page():
    st.title("Đăng ký tài khoản")
    
    username=st.text_input("Tên đăng nhập")
    password=st.text_input("Mật khẩu",type="password")
    confirm=st.text_input("Xác nhận mật khẩu",type="password")
    
    if st.button("Đăng ký"):
        if not username or not password:
            st.warning("Vui lòng nhập đầy đủ thông tin")
        elif password !=confirm:
            st.error("Mật khẩu xác nhận không khớp")
        elif users_col.find_one({"username":username}):
            st.error("Tên đăng nhập đã tồn tại")
        else:
            hashed_pw = generate_password_hash(password)
            users_col.insert_one({
                "username": username,
                "password": hashed_pw,
                "created_at": datetime.now()
            })
            st.success("Đăng ký thành công! Hãy đăng nhập.")
            st.session_state.page = "login"

    st.markdown("---")
    if st.button("Đã có tài khoản? Đăng nhập"):
        st.session_state.page = "login"
