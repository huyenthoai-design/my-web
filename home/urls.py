from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.trangchu),
    path('child1/', views.child1),
    path('child2/', views.child2),
    path('child3/', views.child3),
    path('minigames/', views.minigames),
]
