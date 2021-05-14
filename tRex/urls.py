from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='trex'),
    path('maxscore/', views.max_score, name='trex_max_score'),
]
