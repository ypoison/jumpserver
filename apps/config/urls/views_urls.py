# coding:utf-8
from django.urls import path
from .. import views

app_name = 'config'

urlpatterns = [
    path('node-records/', views.NodeRecordListView.as_view(), name='node-record-list'),
    path('node-config/create/', views.NodeConfigCreateView.as_view(), name='node-config-create'),
    path('node-config/<uuid:pk>/', views.NodeDetailView.as_view(), name='node-config-detail'),
    path('node-config/<uuid:pk>/update/', views.NodeUpdateView.as_view(), name='node-config-update'),

]
