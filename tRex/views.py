from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import MaxScore
import json


@login_required
def index(request):
    if MaxScore.objects.filter(user=request.user):
        return render(request, 'trex_index.html')
    else:
        MaxScore.objects.create(user=request.user)
        return render(request, 'trex_index.html')


@login_required
@api_view(['GET', 'POST'])
def max_score(request):
    if request.method == 'GET':
        return Response(data={'maxScore': MaxScore.objects.get(user=request.user).score}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        userData = MaxScore.objects.get(user=request.user)
        userData.score = request.POST['maxScore']
        userData.save()
        return Response(status=status.HTTP_200_OK)


@login_required
def leader_board(request):
    if request.method == 'GET':
        db = MaxScore.objects.order_by('-score').values('user__username', 'score')
        userScore = MaxScore.objects.filter(user=request.user).values('user__username', 'score')[0]
        return render(request, 'trex_leaderboard.html', {'data': json.dumps(list(db[0:50])), 'userScore': userScore, 'userRank': list(db).index(userScore) + 1})
