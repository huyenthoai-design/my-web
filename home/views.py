from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse

import bcrypt
from .models import UserAccount
from django.contrib import messages

# 1. Trang chủ/gốc
def base(request):
    return render(request, 'base.html')

# 2. Xử lý Đăng nhập
def login_view(request):
    if request.method == "POST":
        un = request.POST.get('username')
        pw = request.POST.get('password')

        # Tìm trong MongoDB xem có ai tên username này không
        user = UserAccount.objects(username=un).first()

        # Nếu tìm thấy người dùng và mật khẩu khớp (dùng bcrypt để giải mã)
        if user and bcrypt.checkpw(pw.encode('utf-8'), user.password.encode('utf-8')):
            # "Đóng dấu" vào trình duyệt để nhớ rằng người này đã vào cửa
            request.session['user_id'] = str(user.id)
            request.session['username'] = user.username
            request.session['full_name'] = user.full_name
            return render(request, 'base.html') # Đưa họ về trang chủ
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng!")
            
    return render(request, 'login.html')

# 3. Trang cá nhân (Chỉ cho phép vào nếu đã "có dấu" Session)
def profile_view(request):
    if not request.session.get('user_id'):
        return redirect('login')
    return render(request, 'profile.html')

# 4. Đăng xuất (Xóa dấu Session)
def logout_view(request):
    request.session.flush()
    return render(request, 'base.html')


# Create your views here.
#def child1(request):
    #return render(request, 'base.html')

# def base ở trên

def trangchu(request):
    return render(request, 'trangchu.html')

def gioithieu(request):
    return render(request, 'gioithieu.html')

def lienhe(request):
    return render(request, 'lienhe.html')

def ping(request):
    return render(request, 'ping.html')

def phongtrao(request):
    return render(request, 'phongtrao.html')

def monhoc(request):
    return render(request, 'monhoc.html')

def sinhhoc(request):
    return render(request, 'sinhhoc.html')

def lichsu(request):
    return render(request, 'lichsu.html')

def minigames(request):
    return render(request, 'minigames.html')

def chuyenchuake(request):
    return render(request, 'chuyenchuake.html')
