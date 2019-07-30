# coding:utf-8
from django.urls import path
from .. import views

app_name = 'cmis'

urlpatterns = [
    path('account/', views.AccountListView.as_view(), name='account-list'),
    path('account/create/', views.AccountCreateView.as_view(), name='account-create'),
    path('account/<uuid:pk>/update/', views.AccountUpdateView.as_view(), name='account-update'),
    path('account/<uuid:pk>/', views.AccountDetailView.as_view(), name='account-detail'),

    path('chost/create/', views.CHostCreateView.as_view(), name='chost-create'),

    path('cdn/', views.CDNDomainListView.as_view(), name='cdn-list'),
    path('cdn/create/', views.CDNDomainCreateView.as_view(), name='cdn-create'),
    path('cdn/<uuid:pk>/', views.CDNDomainDetailView.as_view(), name='cdn-detail'),

    path('cdn/fresh/', views.CDNFreshListView.as_view(), name='cdn-fresh-list'),
    path('cdn/fresh/create/', views.CDNFreshCreateView.as_view(), name='cdn-fresh-create'),
]
