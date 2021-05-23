from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='cu_index'),
    path('reports/', views.reports, name='cu_reports'),
]
