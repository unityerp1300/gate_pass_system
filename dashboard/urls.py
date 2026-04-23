from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.index, name='dashboard'),
    path('hd-stats/', views.hd_stats, name='hd_stats'),
]
