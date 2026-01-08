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

    path('minigames/', views.minigames, name='minigames'),

    path('chuyenchuake/', views.chuyenchuake, name='chuyenchuake'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),

    path('update-duration/', views.update_duration_view, name='update_duration'),
]
