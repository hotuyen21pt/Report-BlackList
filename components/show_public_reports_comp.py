import streamlit as st
from services.report_service import vote_report  # Hàm xử lý lưu phiếu bầu vào DB
from models.report_models import Vote, VoteType  # Model phiếu bầu và kiểu phiếu
from utils.functions import count_votes, auto_classify  # Hàm đếm phiếu và tự phân loại
from db.connection import reports_col, votes_col  # Kết nối MongoDB
import io
from datetime import datetime, timedelta

def show_public_reports(user_id):
    """
    Hiển thị danh sách các báo cáo công khai (Publish)
    - Người dùng có thể xem chi tiết và bình chọn Whitelist hoặc Blacklist
    - Tự động phân loại báo cáo dựa trên kết quả bình chọn
    """

    st.header("Báo cáo công khai")

    # Gọi hàm tự động phân loại (cập nhật trạng thái báo cáo dựa theo kết quả vote)
    auto_classify(reports_col, votes_col)

    # Lấy tất cả các báo cáo có trạng thái Publish
    public_reports = list(reports_col.find({"status": "Publish"}).sort("created_at",-1))

    # Nếu không có báo cáo nào
    if not public_reports:
        st.info("Chưa có báo cáo công khai.")
        return

    # Duyệt qua từng báo cáo công khai
    for report in public_reports:
        st.subheader(report["title"])
        # Tính số ngày còn lại
        delta = timedelta(days=30) - (datetime.now() - report["created_at"])
        remain = max(delta.days, 0)
        st.write(f"Còn lại: {remain} ngày")

        st.write(f"Mô tả: {report["description"]}")
        st.write(f"Danh mục: {report["category"]}")
        if report.get("category") in ["Phone Number", "Personnel / KOL", "Company", "Event"]:
            st.write(f"Chi tiết: {report.get('detail', 'Không có thông tin chi tiết')}")
        # Đếm số lượng bình chọn Whitelist và Blacklist
        wl, bl = count_votes(report["report_id"], votes_col)
        st.write(f"Số phiếu Whitelist: {wl} | Số phiếu Blacklist: {bl}")

        # Hiển thị bằng chứng nếu có (ảnh, audio hoặc video)
        if report.get("proof_data"):
            if report.get("proof_type") == "image":
                st.image(io.BytesIO(report["proof_data"]))
            elif report.get("proof_type") == "video":
                st.video(io.BytesIO(report["proof_data"]))
            elif report.get("proof_type") == "audio":
                st.audio(io.BytesIO(report["proof_data"]))

        # Hai nút bình chọn Whitelist / Blacklist hiển thị song song
        col1, col2 = st.columns(2)

        # Nút bình chọn Whitelist
        with col1:
            if st.button("Vote Whitelist", key=f"whitelist_{report["report_id"]}"):
                vote = Vote(report["report_id"], user_id, VoteType.Whitelist)
                vote_report(vote)
                st.rerun()

        # Nút bình chọn Blacklist
        with col2:
            if st.button("Vote Blacklist", key=f"blacklist_{report["report_id"]}"):
                vote = Vote(report["report_id"], user_id, VoteType.Blacklist)
                vote_report(vote)
                st.rerun()