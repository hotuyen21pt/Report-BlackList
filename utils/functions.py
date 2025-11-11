from datetime import datetime, timedelta
from db.connection import reports_col, votes_col
from models.report_models import Status


def count_votes(report_id, votes_col):
    """
    Đếm số lượng phiếu Whitelist và Blacklist cho một báo cáo.

    Tham số:
        report_id (str): ID của báo cáo.
        votes_col (Collection): Collection chứa dữ liệu bình chọn.
    """
    votes = list(votes_col.find({"report_id": report_id}))
    whitelist_count = sum(1 for v in votes if v["vote_type"] == "Whitelist")
    blacklist_count = sum(1 for v in votes if v["vote_type"] == "Blacklist")
    return whitelist_count, blacklist_count


def auto_classify(reports_col, votes_col):
    """
    Tự động phân loại báo cáo thành Blacklist nếu sau 30 ngày kể từ ngày đăng,
    số phiếu Blacklist nhiều hơn Whitelist.

    Tham số:
        reports_col (Collection): Collection chứa dữ liệu báo cáo.
        votes_col (Collection): Collection chứa dữ liệu bình chọn.
    """
    # Lấy các báo cáo đang ở trạng thái Publish
    reports = list(reports_col.find({"status": Status.Publish.value}))

    for report in reports:
        created_at = report.get("created_at")
        if not created_at:
            continue

        # Chuyển đổi kiểu thời gian nếu được lưu dạng chuỗi
        if isinstance(created_at, str):
            try:
                created_at = datetime.fromisoformat(created_at)
            except ValueError:
                continue

        # Bỏ qua nếu chưa đủ 30 ngày kể từ khi đăng
        if datetime.now() - created_at < timedelta(days=30):
            continue

        # Lấy số lượng phiếu Whitelist / Blacklist
        whitelist, blacklist = count_votes(report["report_id"], votes_col)

        # Nếu Blacklist nhiều hơn thì đổi trạng thái report
        if blacklist > whitelist:
            reports_col.update_one(
                {"report_id": report["report_id"]},
                {
                    "$set": {
                        "status": Status.Blacklist.value,
                        "updated_at": datetime.now()
                    }
                }
            )


def edit_report(reports_col, report_id, user_id,
                title, description, category,detail,
                status, proof_data, proof_type, proof_link):
    """
    Cập nhật thông tin một báo cáo nếu người dùng là chủ sở hữu của báo cáo đó.

    Tham số:
        reports_col (Collection): Collection chứa dữ liệu báo cáo.
        report_id (str): ID báo cáo cần sửa.
        user_id (str): ID người dùng đang thực hiện chỉnh sửa.
        title, description, category, status, proof_data, proof_type, proof_link: thông tin mới.
    """
    report = reports_col.find_one({"report_id": report_id})
    if not report:
        return False, "Report không tồn tại"

    if report["user_id"] != user_id:
        return False, "Bạn không có quyền chỉnh sửa report này"

    update_fields = {}
    if title:
        update_fields["title"] = title
    if description:
        update_fields["description"] = description
    if category:
        update_fields["category"] = category
    if detail:
        update_fields["detail"] = detail
    if status:
        update_fields["status"] = status
    if proof_data:
        update_fields["proof_data"] = proof_data
    if proof_type:
        update_fields["proof_type"] = proof_type
    if proof_link:
        update_fields["proof_link"] = proof_link

    if update_fields:
        update_fields["updated_at"] = datetime.now()
        reports_col.update_one({"report_id": report_id}, {"$set": update_fields})

    return True, "Cập nhật report thành công"

def delete_report(reports_col,report_id,user_id):
    report = reports_col.find_one({"report_id": report_id})
    if not report:
        return False, "Report không tồn tại"

    if report["user_id"] != user_id:
        return False, "Bạn không có quyền xóa report này"

    # Xóa vĩnh viễn 
    reports_col.delete_one({"report_id": report_id})
    return True, "Đã xóa report thành công"