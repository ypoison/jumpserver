# coding:utf-8
from django.urls import path
from .. import views

app_name = 'domain-name'

urlpatterns = [
    path('domain-name/', views.DomainNameListView.as_view(), name='domain-name-list'),
    path('domain-name/create/', views.DomainNameCreateView.as_view(), name='domain-name-create'),
    path('domain-name/<uuid:pk>/', views.DomainNameDetailView.as_view(), name='domain-name-detail'),
    path('domain-name/<uuid:pk>/update/', views.DomainNameUpdateView.as_view(), name='domain-name-update'),

    path('domain-name/<uuid:pk>/records/', views.DomainNameRecordsListView.as_view(), name='records-list'),
    path('domain-name/<uuid:pk>/record/create/', views.DomainNameRecordCreateView.as_view(), name='record-create'),
    path('domain-name/record/<uuid:pk>/update/', views.DomainNameRecordUpdateView.as_view(), name='record-update'),

    path('account/', views.DomainNameAccountListView.as_view(), name='account-list'),
    path('account/create/', views.DomainNameAccountCreateView.as_view(), name='account-create'),
    path('account/<uuid:pk>/update/', views.DomainNameAccountUpdateView.as_view(), name='account-update'),
    path('account/<uuid:pk>/', views.DomainNameAccountDetailView.as_view(), name='account-detail'),
]
