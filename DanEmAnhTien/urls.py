"""
URL configuration for DanEmAnhTien project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from home import views as home
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('home.urls')),
    path('trangchu/', include('home.urls')),
    path('gioithieu/', include('home.urls')),
    path('lienhe/', include('home.urls')),

    path('ping/', include('home.urls')),
    
    path('phongtrao/', include('home.urls')),
    
    path('monhoc/', include('home.urls')),
        path('sinhhoc/', include('home.urls')),
        path('lichsu/', include('home.urls')),

    path('minigames/', include('home.urls')),
        path('game_so_sanh_so/', include('home.urls')),

    path('chuyenchuake/', include('home.urls')),

    path('profile/', include('home.urls')),
    
    # Các url cho JWT Token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]