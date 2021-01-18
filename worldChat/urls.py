from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='world_chat'),
    path('chat/', views.chat),
]