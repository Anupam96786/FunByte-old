from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ttt'),
    path('single/', views.single_options, name='ttt_single_play'),
    path('single/<str:player_sign>/<str:level>', views.single_play, name='ttt_single_play'),
    path('maxscore/', views.max_score, name='ttt_max_score'),
    path('multi/offline/', views.multi_offline, name='ttt_multi_offline'),
]