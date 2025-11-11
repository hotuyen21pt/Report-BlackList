import streamlit as st
from db.connection import reports_col
import io

def show_blacklist_page():
    st.title("Danh sách Blacklist")

    # Lấy tất cả báo cáo có trạng thái Blacklist
    blacklist_reports = list(reports_col.find({"status": "Blacklist"}))

    if not blacklist_reports:
        st.info("Chưa có báo cáo Blacklist nào.")
        return

    for report in blacklist_reports:
        st.subheader(report.get("title", "Không có tiêu đề"))
        st.write(f"Mô tả: {report.get('description', 'Không có mô tả')}")
        st.write(f"Danh mục: {report.get('category', 'Không xác định')}")

        # Hiển thị bằng chứng (nếu có)
        proof_data = report.get("proof_data")
        proof_type = report.get("proof_type")

        if proof_data:
            if proof_type == "image":
                st.image(io.BytesIO(proof_data))
            elif proof_type == "video":
                st.video(io.BytesIO(proof_data))

        # Nếu không có dữ liệu nhúng nhưng có proof_link, hiển thị link
        elif report.get("proof_url"):
            st.markdown(f"[Xem bằng chứng]({report['proof_url']})")

        st.markdown("---")
