from django.db import models

# Create your models here.
import bcrypt
from home.models import UserAccount

# 1. Chuẩn bị dữ liệu
username = "huyenthoai"
password = "huyenthoai123" # Thay bằng mật khẩu bạn muốn cấp
email = "0945799112thoai@gmail.com"

# 2. Mã hóa mật khẩu (Bắt buộc để đăng nhập được)
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# 3. Lưu trực tiếp vào MongoDB
# Lệnh này sẽ tự tạo Database 'sudiala1' và Collection 'users' nếu chưa có
try:
    new_user = UserAccount(username=username, password=hashed, email=email)
    new_user.save()
    print("--- TẠO TÀI KHOẢN THÀNH CÔNG! ---")
    print(f"User: {username}")
except Exception as e:
    print(f"Lỗi rồi: {e}")