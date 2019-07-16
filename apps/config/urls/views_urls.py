# coding:utf-8
from django.urls import path
from .. import views

app_name = 'config'

urlpatterns = [
    path('node-config/', views.NodeConfigListView.as_view(), name='node-config-list'),

    path('node-config/web-config/', views.NodeConfigWEBConfigListView.as_view(), name='web-config-list'),
    path('node-config/web-config/create/', views.NodeConfigWEBConfigCreateView.as_view(), name='web-config-create'),
]
