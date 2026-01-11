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
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserHistory
from collections import defaultdict
import datetime

# --- HÀM 1: HIỂN THỊ LỊCH SỬ (CHỈ CẦN 1 HÀM NÀY) ---
def history_view(request):
    if not request.session.get('user_id'):
        return redirect('login')
    
    uid = request.session['user_id']
    
    # 1. Lấy TẤT CẢ dữ liệu để tính số liệu tổng quát và biểu đồ
    all_histories = UserHistory.objects(user_id=uid)
    total_visits = all_histories.count()
    total_sec = sum(item.duration for item in all_histories)
    
    # Tính toán chuỗi thời gian hiển thị
    total_h = total_sec // 3600
    total_m = (total_sec % 3600) // 60
    total_time_str = f"{total_h} giờ {total_m} phút"

    # 2. Lấy danh sách URL chưa bị ẩn (is_visible=True) để hiện ở bảng
    visible_histories = UserHistory.objects(user_id=uid, is_visible=True).order_by('-access_time')

    # Xử lý múi giờ +7 cho danh sách hiển thị
    # QUAN TRỌNG: Tạo một danh sách mới để đảm bảo biến vn_time được lưu lại
    processed_histories = []
    for item in visible_histories:
        # Cộng 7 giờ vào access_time
        item.vn_time = item.access_time + datetime.timedelta(hours=7)
        processed_histories.append(item)

    # 3. Xử lý dữ liệu biểu đồ (dùng all_histories để không mất dữ liệu biểu đồ)
    daily_data = defaultdict(int)
    for item in all_histories:
        vn_t = item.access_time + datetime.timedelta(hours=7)
        date_str = vn_t.strftime('%d/%m/%Y')
        daily_data[date_str] += item.duration

    # Lấy 7 ngày gần nhất
    sorted_days = sorted(daily_data.keys(), key=lambda x: datetime.datetime.strptime(x, '%d/%m/%Y'))[-7:]
    minutes_data = [round(daily_data[day] / 60, 1) for day in sorted_days]

    return render(request, 'history.html', {
        'histories': processed_histories,
        'total_visits': total_visits,
        'total_time_str': total_time_str,
        'chart_labels': sorted_days,
        'chart_data': minutes_data,
    })

# --- HÀM 2: LÀM SẠCH DANH SÁCH (CHUYỂN SANG ẨN) ---
def clear_history_view(request):
    if request.method == "POST" and request.session.get('user_id'):
        uid = request.session['user_id']
        # Đánh dấu tất cả là ẩn thay vì xóa
        UserHistory.objects(user_id=uid, is_visible=True).update(set__is_visible=False)
    return redirect('history')

# --- HÀM 3: UPDATE DURATION NHẬN DỮ LIỆU THỜI GIAN TỪ JAVASCRIPT (CHẠY NGẦM) ---
@csrf_exempt
def update_duration_view(request):
    if request.method == "POST" and request.session.get('user_id'):
        uid = request.session['user_id']
        url = request.POST.get('url')
        # Lấy số giây từ Javascript gửi về
        try:
            duration = int(float(request.POST.get('duration', 0)))
        except ValueError:
            duration = 0

        if duration > 2:  # Chỉ lưu nếu ở lại trang lâu hơn 2 giây
            UserHistory(
                user_id=uid,
                url=url,
                access_time=datetime.datetime.utcnow(),
                duration=duration
            ).save()
            return JsonResponse({"status": "success"})
            
    return JsonResponse({"status": "failed"}, status=400)

# 7. lưu dữ liệu khi chơi game so sánh số
from django.http import JsonResponse
from .models import UserAccount

# --- HÀM 1: ---
def save_game_score(request):
    if request.method == "POST" and request.session.get('user_id'):
        uid = request.session['user_id']
        new_points = int(request.POST.get('points', 0))

        # Tìm người dùng trực tiếp trong bảng User
        user = UserAccount.objects(id=uid).first()
        if user:
            # Cộng dồn điểm vào trường total_score của User
            user.total_score += new_points
            user.save() # Lưu lại vào MongoDB
            
            return JsonResponse({
                "status": "success", 
                "total_score": user.total_score
            })
    return JsonResponse({"status": "failed"}, status=400)

# --- HÀM 2: ---
@csrf_exempt # Nếu bạn dùng decorator này thì không cần header CSRF cho hàm này
def update_duration_view(request):
    if request.method == "POST":
        # Sử dụng .get() và cung cấp giá trị mặc định để tránh lỗi 400
        url = request.POST.get('url', 'unknown')
        duration_raw = request.POST.get('duration', 0)
        
        try:
            duration = int(float(duration_raw))
        except (ValueError, TypeError):
            duration = 0
            
        # ... logic lưu vào MongoDB giữ nguyên ...
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed"}, status=400)


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

def minigames_view(request):
    return render(request, 'minigames.html')

def game_so_sanh_so(request):
    user_points = 0
    uid = request.session.get('user_id')
    
    if uid:
        user = UserAccount.objects(id=uid).first()
        if user:
            # Lấy tổng điểm hiện có để hiển thị khi bắt đầu vào game
            user_points = getattr(user, 'total_score', 0)
            
    # Gửi biến sang file HTML
    return render(request, 'game_so_sanh_so.html', {'user_score': user_points})

def chuyenchuake(request):
    return render(request, 'chuyenchuake.html')
