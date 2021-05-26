from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('mailconfirmation/<str:token>', views.mail_confirmation),
    path('logout/', views.user_logout, name='logout'),
    path('changepassword/', views.change_password, name='change_password'),
    path('forgotpassword/', views.forgot_password, name='forgot_password'),
    path('fpchange/<str:token>', views.fp_change),
    path('profile/<str:username>', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('getverificationlink/', views.get_verification_link, name='get_verification_link'),
]
