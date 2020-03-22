# coding:utf-8
from django.urls import path
from .. import views

app_name = 'online'

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]