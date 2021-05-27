from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ttt'),
    path('single/', views.single_options, name='ttt_single_play'),
    path('single/<str:player_sign>/<str:level>', views.single_play, name='ttt_single_play'),
    path('maxscore/', views.max_score, name='ttt_max_score'),
    path('multi/offline/', views.multi_offline, name='ttt_multi_offline'),
    path('leaderboard/', views.leader_board, name='ttt_leader_board'),
    path('leaderboardscore/', views.leader_board_score, name='ttt_leader_board_score'),
    path('leaderboard/<str:username>/<str:level>', views.leader_board_user, name='ttt_leader_board_user'),
    path('multi/online/', views.multi_online, name='ttt_multi_online'),
    path('multi/online/<str:roomId>', views.multi_online_id, name='ttt_multi_online_id'),
]
