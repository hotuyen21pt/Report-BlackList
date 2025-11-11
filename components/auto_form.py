import re
import streamlit as st
from google import genai
from google.genai import types
from services.report_service import create_report
from models.report_models import Report, Status
from bson.binary import Binary
import io


# ---------------- HÀM TRÍCH XUẤT THÔNG TIN BẰNG REGEX ----------------
def extract_fields_with_regex(text):
    patterns = {
        "title": r"(?:Tiêu đề|Title)\s*[:\-]\s*(.+)",
        "description": r"(?:Mô tả|Description)\s*[:\-]\s*(.+)",
        "category": r"(?:Danh mục|Category)\s*[:\-]\s*(.+)",
        "detail": r"(?:Chi tiết|Detail)\s*[:\-]\s*(.+)"
    }
    extracted = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        extracted[key] = match.group(1).strip() if match else ""
    return extracted

# ---------------- FORM TỰ ĐỘNG TẠO BÁO CÁO ----------------
def show_auto_report_form(user_id):
    st.title("Tạo báo cáo tự động")

    # Nút hiển thị form (key duy nhất)
    if st.button("Tạo báo cáo mới", key="btn_create_report"):
        st.session_state.show_form = True

    # Kiểm tra trạng thái form
    if st.session_state.get("show_form", False):
        GEMINI_API_KEY = "AIzaSyD_hssyeWCwEB05TpKP8e9DUAmKNxi9AmM"
        client = genai.Client(api_key=GEMINI_API_KEY)

        # Upload file
        uploaded_file = st.file_uploader(
            "Tải lên bằng chứng (ảnh, video, pdf, txt...)",
            type=["jpg", "jpeg", "png", "mp4", "pdf", "wav", "mp3", "txt"],
            key="file_uploader_auto_form"
        )

        # Lưu file vào session_state
        if uploaded_file:
            # Đọc lại dữ liệu & reset con trỏ về đầu
            uploaded_file.seek(0)
            file_bytes = uploaded_file.read()
            mime_type = uploaded_file.type or "application/octet-stream"

            # Lưu vào session
            st.session_state.file_bytes = file_bytes
            st.session_state.mime_type = mime_type
            st.session_state.proof_data = Binary(file_bytes)

            # Hiển thị preview đúng kiểu
            if mime_type.startswith("image/"):
                st.image(io.BytesIO(file_bytes), use_container_width=True)
            elif mime_type.startswith("video/"):
                st.video(io.BytesIO(file_bytes))
            elif mime_type.startswith("audio/"):
                st.audio(io.BytesIO(file_bytes))
            else:
                st.info(f"File MIME không được hỗ trợ để hiển thị: {mime_type}")

        # Nút phân tích nội dung (key duy nhất)
        if uploaded_file and st.button("Phân tích nội dung", key="btn_analyze_content"):
            try:
                with st.spinner("Đang phân tích bằng chứng..."):
                    prompt = """
                    Bạn là hệ thống AI phân tích báo cáo blacklist.
                    Hãy đọc nội dung trong tệp và trích xuất các thông tin sau:

                    Tiêu đề: <tóm tắt ngắn vụ việc>
                    Mô tả: <mô tả chi tiết>
                    Danh mục: <Phone Number / Personnel / Company / Event>
                    Chi tiết: <thông tin cụ thể về danh mục>

                    Chỉ trả về đúng 4 dòng theo format trên.
                    Không thêm ký tự hoặc giải thích nào khác.
                    """
                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[
                            prompt,
                            types.Part.from_bytes(
                                data=st.session_state.file_bytes,
                                mime_type=st.session_state.mime_type
                            )
                        ]
                    )
                    st.session_state.ai_result = response.text.strip()
            except Exception as e:
                st.error(f"Lỗi khi phân tích: {e}")

        # Nếu đã có kết quả AI, hiển thị form lưu báo cáo
        if st.session_state.get("ai_result"):
            st.subheader("Kết quả phân tích")
            st.text(st.session_state.ai_result)

            data = extract_fields_with_regex(st.session_state.ai_result)
            st.subheader("Thông tin trích xuất")

            if data.get("title"):
                with st.form("save_report_form"):
                    title = st.text_input("Tiêu đề", data["title"], key="input_title")
                    description = st.text_area("Mô tả", data["description"], key="input_description")
                    category = st.text_input("Danh mục", data["category"], key="input_category")
                    detail = st.text_input("Chi tiết", data["detail"], key="input_detail")
                    proof_data = st.session_state.get("proof_data")
                    proof_type = st.session_state.get("mime_type")
                    proof_link= st.session_state.get("proof_link")                  
                    col1,col2=st.columns(2)
                    with col1:
                        draft_btn=st.form_submit_button("Save as Draft",key="btn_draft")
                    with col2:
                        publish_btn=st.form_submit_button("Publish",key="btn_publish")                     
                    if draft_btn or publish_btn:
                        if not title or not description:
                            st.warning("Tiêu đề và mô tả không được để trống.")
                        else:
                            status="Draft" if draft_btn else "Publish"  
                            proof_data = st.session_state.get("proof_data")
                            mime_type = st.session_state.get("mime_type")
                            report = Report(
                                user_id=user_id,
                                title=title,
                                description=description,
                                category=category,
                                detail=detail,
                                proof_data=proof_data,
                                proof_link=proof_link,
                                proof_type=mime_type,
                            )
                            report.status = Status(status)
                            report_id = create_report(report)
                            st.success(f"Báo cáo đã lưu thành công! ID: {report_id}")
                            st.session_state.show_form = False
                            st.session_state.ai_result = None
                            st.rerun()
            else:
                st.warning("Không tìm thấy dữ liệu hợp lệ. Kiểm tra format phản hồi của AI.")

        # Nút hủy ngoài form (key duy nhất)
        if st.button("Hủy", key="btn_cancel"):
            st.session_state.show_form = False
            st.session_state.ai_result = None
            st.info("Đã hủy tạo báo cáo.")
            st.rerun()
