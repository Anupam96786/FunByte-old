from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import MaxScore
import json


def index(request):
    return render(request, 'trex_index.html')


@login_required
@api_view(['GET', 'POST'])
def max_score(request):
    if request.method == 'GET':
        return Response(data={'maxScore': MaxScore.objects.get_or_create(user=request.user)[0].score}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        userData = MaxScore.objects.get_or_create(user=request.user)[0]
        userData.score = request.POST['maxScore']
        userData.save()
        return Response(status=status.HTTP_200_OK)


def leader_board(request):
    if request.method == 'GET':
        db = MaxScore.objects.order_by('-score').values('user__username', 'score')
        if request.user.is_authenticated:
            userScore = db.filter(user=request.user)[0]
            return render(request, 'trex_leaderboard.html', {'data': json.dumps(list(db[0:50])), 'userScore': userScore, 'userRank': list(db).index(userScore) + 1})
        else:
            return render(request, 'trex_leaderboard.html', {'data': json.dumps(list(db[0:50])), 'userScore': {}, 'userRank': {}})


def leader_board_user(request, username):
    db = MaxScore.objects.order_by('-score').values('user__username', 'score')
    user = db.filter(user__username=username)[0]
    return render(request, 'trex_leaderboard_user.html', {'rank': list(db).index(user) + 1, 'username': username, 'score': user['score']})
