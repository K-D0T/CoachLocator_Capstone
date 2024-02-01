from django.urls import path
from django.contrib import admin
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('nearme', views.nearme, name='nearme'),
    path('becomecoach', views.becomecoach, name='becomecoach'),
    path('coachdetail/<int:coach_id>', views.coach_detail, name='coachdetail'),
]
