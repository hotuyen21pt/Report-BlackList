# db/connection.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Lấy thông tin cấu hình từ biến môi trường hoặc dùng giá trị mặc định
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://hotuyen21pt:21022004a@cluster0.kgalw36.mongodb.net/?appName=Cluster0")
DB_NAME = os.getenv("DB_NAME", "blacklist_app_db")

# Tạo kết nối đến MongoDB
client = MongoClient(MONGO_URI)

# Chọn cơ sở dữ liệu
db = client[DB_NAME]

# Các collection (bảng) chính được sử dụng trong ứng dụng
reports_col = db["reports"]  # Lưu thông tin báo cáo
votes_col = db["votes"]      # Lưu thông tin bình chọn
users_col = db["users"]      # Lưu thông tin người dùng