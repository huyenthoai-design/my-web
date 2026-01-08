from django.db import models

# Create your models here.
from mongoengine import Document, StringField, EmailField, DateTimeField, IntField, ReferenceField
import datetime

class UserAccount(Document):
    meta = {'collection': 'users'} # Dữ liệu sẽ lưu vào bảng 'users'
    
    username = StringField(required=True, unique=True)
    password = StringField(required=True) # Đây là nơi lưu mật khẩu đã mã hóa
    full_name = StringField()
    email = EmailField()

    def __str__(self):
        return self.username


class UserHistory(Document):
    user_id = StringField(required=True)
    url = StringField()
    access_time = DateTimeField(default=datetime.datetime.utcnow) # Lưu UTC, khi hiện sẽ +7
    duration = IntField(default=0)  # Thời gian ở lại trang tính bằng giây