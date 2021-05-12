from django.conf.urls import handler400, handler403, handler500
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('worldchat/', include('worldChat.urls')),
    path('secretmessage/', include('secretMessage.urls')),
    path('tictactoe/', include('ticTacToe.urls')),
]

handler400 = views.error_400
handler404 = views.error_404
handler403 = views.error_403
handler500 = views.error_500
