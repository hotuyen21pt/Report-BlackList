# models/report_models.py
from enum import Enum
from datetime import datetime, timedelta
import uuid


# Trạng thái của một báo cáo
class Status(str, Enum):
    Draft = "Draft"         # Báo cáo đang ở dạng nháp, chưa công khai
    Publish = "Publish"     # Báo cáo đã công khai
    Blacklist = "Blacklist" # Báo cáo đã được phân loại là Blacklist (tự động)


# Loại phiếu bình chọn
class VoteType(str, Enum):
    Whitelist = "Whitelist"
    Blacklist = "Blacklist"


class Report:
    """
    Lớp mô tả cấu trúc dữ liệu của một báo cáo (Report).
    Dùng để khởi tạo đối tượng báo cáo và chuyển đổi sang dict trước khi lưu vào MongoDB.
    """

    def __init__(self, user_id, title, description, category, detail,
                 proof_data, proof_link=None, proof_type=None):
        # Sinh ID duy nhất cho mỗi báo cáo
        self.report_id = str(uuid.uuid4())

        # Thông tin cơ bản của báo cáo
        self.user_id = user_id
        self.title = title
        self.description = description
        self.category = category
        self.detail = detail

        # Dữ liệu bằng chứng (file hoặc link)
        self.proof_data = proof_data      # File Binary (image/video/audio)
        self.proof_link = proof_link        # Link bằng chứng nếu có
        self.proof_type = proof_type      # Kiểu file: image / video /audio

        # Trạng thái và thời gian
        self.status = Status.Draft        # Mặc định là Draft
        self.created_at = datetime.now()  # Ngày tạo
        self.updated_at = datetime.now()  # Ngày cập nhật
    
    def to_dict(self):
        """
        Chuyển đổi đối tượng Report thành dictionary để lưu vào MongoDB.
        """
        return {
            "report_id": self.report_id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "detail" : self.detail,
            "proof_data": self.proof_data,
            "proof_link": self.proof_link,
            "proof_type": self.proof_type,
            "status": self.status.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class Vote:
    """
    Lớp mô tả cấu trúc dữ liệu của một phiếu bình chọn (Vote).
    Mỗi người dùng có thể vote Whitelist hoặc Blacklist cho một báo cáo cụ thể.
    """

    def __init__(self, report_id, user_id, vote_type):
        self.report_id = report_id        # ID báo cáo được bình chọn
        self.user_id = user_id            # ID người bình chọn
        self.vote_type = vote_type        # Kiểu bình chọn (Whitelist/Blacklist)
        self.created_at = datetime.now()  # Thời gian tạo phiếu

    def to_dict(self):
        """
        Chuyển đổi đối tượng Vote thành dictionary để lưu vào MongoDB.
        """
        return {
            "report_id": self.report_id,
            "user_id": self.user_id,
            "vote_type": self.vote_type.value,
            "created_at": self.created_at
        }
