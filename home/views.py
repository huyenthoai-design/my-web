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
            request.session['email'] = user.email # THÊM DÒNG NÀY: Lấy email từ đối tượng user vừa tìm thấy trong MongoDB
            return render(request, 'trangchu.html') # Đưa họ về trang chủ
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng!")
            
    return render(request, 'login.html')

# 3. Trang cá nhân (Chỉ cho phép vào nếu đã "có dấu" Session)
# home/views.py

def profile_view(request):
    # Kiểm tra nếu chưa đăng nhập thì đá về trang login
    if not request.session.get('user_id'):
        return redirect('login')
    
    # Lấy thông tin từ session đã lưu lúc đăng nhập thành công
    context = {
        'full_name': request.session.get('full_name'),
        'username': request.session.get('username'),
        'email': request.session.get('email') # Lấy email từ session ra
    }
    
    return render(request, 'profile.html', context)

# 4. Đăng xuất (Xóa dấu Session)
def logout_view(request):
    request.session.flush()
    return render(request, 'base.html')

# 5. Sửa thông tin người dùng
def edit_profile_view(request):
    if not request.session.get('user_id'):
        return redirect('login')
    
    # Lấy thông tin hiện tại từ MongoDB
    user = UserAccount.objects(id=request.session['user_id']).first()

    if request.method == "POST":
        # Lấy dữ liệu mới từ Form
        new_full_name = request.POST.get('full_name')
        new_email = request.POST.get('email')

        # Cập nhật vào Database
        user.full_name = new_full_name
        user.email = new_email
        user.save()

        # Cập nhật lại "túi" Session để giao diện đổi tên ngay lập tức
        request.session['full_name'] = new_full_name
        request.session['email'] = new_email

        return redirect('profile') # Lưu xong thì quay về trang cá nhân

    return render(request, 'edit_profile.html', {'user': user})

# 6. Thông tin lịch sử người dùng
from .models import UserHistory
from django.utils import timezone
import datetime

def history_view(request):
    if not request.session.get('user_id'):
        return redirect('login')
    
    uid = request.session['user_id']
    # Lấy lịch sử, sắp xếp mới nhất lên đầu
    histories = UserHistory.objects(user_id=uid).order_by('-access_time')
    
    total_visits = histories.count()
    total_seconds = sum(h.duration for h in histories)
    
    # Tính Tổng giờ : phút
    total_hours = total_seconds // 3600
    total_minutes = (total_seconds % 3600) // 60
    duration_str = f"{total_hours} giờ {total_minutes} phút"

    # Dữ liệu cho biểu đồ (7 ngày gần nhất)
    # Phần này chúng ta sẽ nhóm dữ liệu theo ngày để vẽ Chart
    
    context = {
        'histories': histories,
        'total_visits': total_visits,
        'duration_str': duration_str,
    }
    return render(request, 'history.html', context)

# 6.1 javascript tính giờ
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserHistory
import datetime

@csrf_exempt # Cho phép nhận dữ liệu từ Javascript
def update_duration_view(request):
    if request.method == "POST" and request.session.get('user_id'):
        uid = request.session['user_id']
        url = request.POST.get('url')
        duration = int(float(request.POST.get('duration', 0)))

        if duration > 0:
            # Lưu bản ghi mới vào MongoDB
            UserHistory(
                user_id=uid,
                url=url,
                access_time=datetime.datetime.utcnow(),
                duration=duration
            ).save()
            return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed"}, status=400)

# 6.2 Thể hiện giờ
def history_view(request):
    uid = request.session.get('user_id')
    # Lấy dữ liệu từ MongoDB
    histories = UserHistory.objects(user_id=uid).order_by('-access_time')

    total_visits = histories.count()
    total_sec = sum(h.duration for h in histories)
    
    # Tính giờ/phút
    h = total_sec // 3600
    m = (total_sec % 3600) // 60
    total_time_str = f"{h} giờ {m} phút"

    # Xử lý dữ liệu hiển thị danh sách (Cộng 7 giờ cho đúng giờ VN)
    for item in histories:
        item.local_time = item.access_time + datetime.timedelta(hours=7)

    return render(request, 'history.html', {
        'histories': histories,
        'total_visits': total_visits,
        'total_time_str': total_time_str
    })

# 6.3 Xử lí biểu đồ cho thời gian người dùng
from django.db.models import Sum
from collections import defaultdict

def history_view(request):
    uid = request.session.get('user_id')
    histories = UserHistory.objects(user_id=uid).order_by('-access_time')
    # --- BỔ SUNG ĐOẠN NÀY ĐỂ HẾT LỖI ---
    total_visits = histories.count()
    total_sec = sum(h.duration for h in histories)
    # Tính giờ/phút
    h = total_sec // 3600
    m = (total_sec % 3600) // 60
    total_time_str = f"{h} giờ {m} phút"
    # ----------------------------------
    # --- Xử lý dữ liệu cho Biểu đồ ---
    daily_data = defaultdict(int)
    for h_item in histories:
        # Chuyển về giờ VN để nhóm cho đúng ngày
        vn_time = h.access_time + datetime.timedelta(hours=7)
        date_str = vn_time.strftime('%d/%m/%Y')
        daily_data[date_str] += h.duration

    # Lấy 7 ngày gần nhất (sắp xếp theo thứ tự thời gian tăng dần để vẽ biểu đồ)
    sorted_days = sorted(daily_data.keys(), key=lambda x: datetime.datetime.strptime(x, '%d/%m/%Y'))[-7:]
    
    # Chuyển giây thành phút để biểu đồ dễ nhìn hơn
    minutes_data = [round(daily_data[day] / 60, 1) for day in sorted_days]

    # ... các phần tính toán cũ (total_visits, total_time_str) ...

    return render(request, 'history.html', {
        'histories': histories,
        'total_visits': total_visits,
        'total_time_str': total_time_str,
        'chart_labels': sorted_days, # Các ngày (Trục X)
        'chart_data': minutes_data,  # Số phút (Trục Y)
    })

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
