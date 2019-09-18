# coding:utf-8
from django.urls import path
from .. import views

app_name = 'rbac'

urlpatterns = [
    path('menu/', views.MenuListView.as_view(), name='menu-list'),
    path('menu/create/', views.MenuCreateView.as_view(), name='menu-create'),
    path('menu/<uuid:pk>/update/', views.MenuUpdateView.as_view(), name='menu-update'),

    path('group/', views.GroupListView.as_view(), name='group-list'),

    path('user/', views.UserListView.as_view(), name='user-list'),
]
