from django.db import models

# Create your models here.
from mongoengine import Document, StringField, EmailField, DateTimeField, IntField, ReferenceField, BooleanField
import datetime

class UserAccount(Document):
    meta = {'collection': 'users'} # Dữ liệu sẽ lưu vào bảng 'users'
    
    username = StringField(required=True, unique=True)
    password = StringField(required=True) # Đây là nơi lưu mật khẩu đã mã hóa
    full_name = StringField()
    email = EmailField()
    total_score = IntField(default=0)

    def __str__(self):
        return self.username


class UserHistory(Document):
    user_id = StringField(required=True)
    url = StringField()
    access_time = DateTimeField(default=datetime.datetime.utcnow)
    duration = IntField(default=0)
    is_visible = BooleanField(default=True) # Dòng này giúp chức năng xóa hoạt động
    