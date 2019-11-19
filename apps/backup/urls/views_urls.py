# coding:utf-8
from django.urls import path
from .. import views

app_name = 'backup'

urlpatterns = [
    path('records/', views.RecordsView.as_view(), name='record-list'),
]
