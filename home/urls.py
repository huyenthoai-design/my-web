from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.child1),
]

urlpatterns = [
    path('api/hello/', views.hello),
]
