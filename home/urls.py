from django.urls import path
from django.contrib import admin
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('nearme', views.nearme, name='nearme'),
    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('coachdetail/<int:coach_id>', views.coach_detail, name='coachdetail'),
    path('profile', views.profile, name='profile'),
]
