from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),

    path('trangchu/', views.trangchu, name='trangchu'),
    path('gioithieu/', views.gioithieu, name='gioithieu'),
    path('lienhe/', views.lienhe, name='lienhe'),

    path('ping/', views.ping, name='ping'),

    path('phongtrao/', views.phongtrao, name='phongtrao'),

    path('monhoc/', views.monhoc, name='monhoc'),
        path('sinhhoc/', views.sinhhoc, name='sinhhoc'),
        path('lichsu/', views.lichsu, name='lichsu'),

    path('minigames/', views.minigames_view, name='minigames'),
        path('game_so_sanh_so/', views.game_so_sanh_so, name='game_so_sanh_so'),
        path('save-game-score/', views.save_game_score, name='save_game_score'),

    path('chuyenchuake/', views.chuyenchuake, name='chuyenchuake'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),

    path('history/', views.history_view, name='history'),
    path('update-duration/', views.update_duration_view, name='update_duration'),
    path('clear-history/', views.clear_history_view, name='clear_history'),
]
