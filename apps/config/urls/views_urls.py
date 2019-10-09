# coding:utf-8
from django.urls import path
from .. import views

app_name = 'config'

urlpatterns = [
    path('node-config/', views.NodeConfigListView.as_view(), name='node-config-list'),
    path('app/', views.AppListView.as_view(), name='app-list'),
    path('app/create/', views.AppCreateView.as_view(), name='app-create'),
    path('app/<pk>/update/', views.AppUpdateView.as_view(), name='app-update'),

    path('web-config/', views.NodeConfigWEBConfigListView.as_view(), name='web-config-list'),
    path('web-config/create/', views.NodeConfigWEBConfigCreateView.as_view(), name='web-config-create'),
    path('web-config/bulk/create/', views.WEBConfigBulkCreateView.as_view(), name='web-config-bulk-create'),
]
