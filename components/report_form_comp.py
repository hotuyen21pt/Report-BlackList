import streamlit as st
import io
from bson.binary import Binary

MAX_FILE_SIZE_MB = 200
MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024

def report_form(existing=None):
    """
    Hiển thị form nhập báo cáo (tạo mới hoặc chỉnh sửa).
    KHÔNG chứa nút submit — chỉ return dữ liệu nhập.
    Nếu có existing, sẽ điền sẵn dữ liệu cũ.
    """

    # --- Giá trị mặc định ---
    default_title = existing.get("title", "") if existing else ""
    default_desc = existing.get("description", "") if existing else ""
    default_category = existing.get("category", None) if existing else None
    default_detail = existing.get("detail", "") if existing else ""
    default_link = existing.get("proof_link", "") if existing else ""
    default_status = existing.get("status", "Draft") if existing else "Draft"

    # --- Trường nhập liệu ---
    title = st.text_input("Tiêu đề báo cáo", value=default_title)
    description = st.text_area("Mô tả chi tiết sự việc", value=default_desc)

    options = ["Phone Number", "Personnel / KOL", "Company", "Event"]
    index = options.index(default_category) if default_category in options else 0
    category = st.selectbox("Danh mục báo cáo", options, index=index)

    detail = st.text_input("Chi tiết liên quan", value=default_detail)

    # --- Bằng chứng ---
    st.write("Tải lên bằng chứng (hình ảnh, audio, video)")
    uploaded_file = st.file_uploader(
        "Chọn tệp (tối đa 200MB)",
        type=["png", "jpg", "jpeg", "mp4", "mov", "mp3", "wav", "m4a"],
        key=f"upload_{existing['_id'] if existing else 'new'}"
    )

    proof_data, proof_type = None, None
    if uploaded_file:
        file_bytes = uploaded_file.read()
        if len(file_bytes) > MAX_FILE_SIZE:
            st.warning(" File quá lớn (>200MB).")
        else:
            proof_data = Binary(file_bytes)
            mime = uploaded_file.type.lower()
            if "image" in mime:
                proof_type = "image"
                st.image(io.BytesIO(file_bytes), use_container_width=True)
            elif "video" in mime:
                proof_type = "video"
                st.video(io.BytesIO(file_bytes))
            elif "audio" in mime:
                proof_type = "audio"
                st.audio(io.BytesIO(file_bytes))

    proof_link = st.text_input("Hoặc nhập link bằng chứng", value=default_link)

    # --- Trả dữ liệu ra ngoài ---
    return title, description, category, detail, default_status, proof_data, proof_type, proof_link
