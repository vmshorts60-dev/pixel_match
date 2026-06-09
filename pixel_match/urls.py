"""
URL configuration for untitled17 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from . import views


from django.contrib import admin
from django.urls import path

urlpatterns = [

    path('home/', views.home, name='home'),

    path('login/', views.login_view, name='login'),

    path('register/', views.register, name='register'),

    path('profile/', views.profile, name='profile'),

    path('matches/', views.matches, name='matches'),

    path('matches/<int:profile_id>/',views.matches,name='matches'),


    path('like/<int:user_id>/', views.like_user, name='like_user'),

    path('my-matches/', views.my_matches, name='my_matches'),

    path('chat/<int:user_id>/', views.chat, name='chat'),

path('edit-profile/', views.edit_profile, name='edit_profile'),

path('dashboard/', views.dashboard, name='dashboard'),

path('logout/', views.logout_view, name='logout'),



path(
    'upload-photos/',
    views.upload_photos,
    name='upload_photos'
),

path(
    'skip/<int:profile_id>/',
    views.skip_user,
    name='skip_user'
),

]

