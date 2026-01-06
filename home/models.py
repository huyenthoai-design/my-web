from django.db import models

# Create your models here.
from mongoengine import Document, StringField, EmailField

class UserAccount(Document):
    meta = {'collection': 'users'} # Dữ liệu sẽ lưu vào bảng 'users'
    
    username = StringField(required=True, unique=True)
    password = StringField(required=True) # Đây là nơi lưu mật khẩu đã mã hóa
    full_name = StringField()
    email = EmailField()

    def __str__(self):
        return self.username