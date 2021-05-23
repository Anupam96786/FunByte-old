from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='br_index'),
    path('report/', views.report, name='br_report'),
]
