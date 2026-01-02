from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.base),
    path('trangchu/', views.trangchu),
    path('gioithieu/', views.gioithieu),
    path('lienhe/', views.lienhe),
    path('minigames/', views.minigames),
    path('monhoc/', views.monhoc),
    path('sinhhoc/', views.sinhhoc),
]
