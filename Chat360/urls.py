"""Chat360 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from home import views as home_views
from django.contrib.auth import views as auth_view
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from ChatBot360 import views as ChatBot360_views
from django.contrib.auth import logout
from VideoChat360 import views as VideoChat360_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('register/', home_views.register, name='register'),
    path('user_login/', home_views.user_login, name='user_login'),
    path('user_logout/', home_views.user_logout, name='user_logout'),
    path('features/',home_views.features, name='features'),
    path('features/ChatBot360/',include('ChatBot360.urls')),
    path('get-value', ChatBot360_views.getValue, name='getValue'),
    path('features/profile/', home_views.profile, name='profile'),
    path('features/VideoChat360/', VideoChat360_views.VideoChat360, name='VideoChat360'),
    path('features/VideoChat360/friendVClobby', VideoChat360_views.friendVClobby, name='friendVClobby'),
    path('get_token/',VideoChat360_views.getToken,name='getToken'),
    path('friendVC/', VideoChat360_views.friendVC, name='friendVC'),
    path('features/VideoChat360/groupVC', VideoChat360_views.groupVC, name='groupVC')
    
    

   
]

urlpatterns+= staticfiles_urlpatterns()