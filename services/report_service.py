# services/report_service.py
from db.connection import reports_col, votes_col
from models.report_models import Report, Vote
from datetime import datetime

def create_report(report: Report):
    """
    Hàm tạo mới một báo cáo và lưu vào MongoDB.

    Tham số:
        report (Report): Đối tượng báo cáo cần lưu.

    Trả về:
        str: ID của báo cáo vừa được tạo.
    """
    reports_col.insert_one(report.to_dict())
    return report.report_id


def vote_report(vote: Vote):
    """
    Hàm thêm hoặc cập nhật bình chọn (vote) của người dùng cho một báo cáo.

    Nếu người dùng đã vote trước đó thì cập nhật vote_type mới,
    ngược lại sẽ tạo mới một bản ghi vote.

    Tham số:
        vote (Vote): Đối tượng vote gồm report_id, user_id và loại vote.

    Trả về:
        bool: True nếu thực hiện thành công.
    """
    # Kiểm tra xem người dùng đã từng vote cho report này chưa
    existing_vote = votes_col.find_one({
        "report_id": vote.report_id,
        "user_id": vote.user_id
    })

    if existing_vote:
        # Cập nhật loại vote và thời gian
        votes_col.update_one(
            {"report_id": vote.report_id, "user_id": vote.user_id},
            {"$set": {
                "vote_type": vote.vote_type.value,
                "created_at": datetime.now()
            }}
        )
    else:
        # Thêm vote mới
        votes_col.insert_one(vote.to_dict())

    return True
