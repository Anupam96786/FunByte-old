from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='secret_message'),
    path('send/<str:user_id>', views.send_msg, name='secret_message_send'),
    path('delmsg/', views.del_msg, name='secret_message_delmsg')
]
