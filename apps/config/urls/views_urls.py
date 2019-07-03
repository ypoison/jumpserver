# coding:utf-8
from django.urls import path
from .. import views

app_name = 'config'

urlpatterns = [
    path('high-anti/', views.NodeListView.as_view(), name='high-anti-list'),
    path('high-anti/create/', views.NodeCreateView.as_view(), name='high-anti-create'),
    path('high-anti/<uuid:pk>/', views.NodeDetailView.as_view(), name='high-anti-detail'),
    path('high-anti/<uuid:pk>/update/', views.NodeUpdateView.as_view(), name='high-anti-update'),

]
