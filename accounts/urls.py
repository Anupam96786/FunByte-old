from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('useractivation/<str:token>', views.user_activation),
    path('logout/', views.user_logout, name='logout'),
    path('changepassword/', views.change_password, name='change_password'),
    path('forgotpassword/', views.forgot_password, name='forgot_password'),
    path('fpchange/<str:token>', views.fp_change),
]
