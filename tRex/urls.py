from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='trex'),
    path('maxscore/', views.max_score, name='trex_max_score'),
    path('leaderboard/', views.leader_board, name='trex_leaderboard'),
    path('leaderboard/<str:username>', views.leader_board_user, name='trex_leaderboard_user'),
]
