from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import MaxScore


def index(request):
    return render(request, 'ttt_index.html')


@login_required
def single_options(request):
    return render(request, 'ttt_single_options.html')


@login_required
def single_play(request, player_sign, level):
    sign = ['X', 'O']
    l = ['easy', 'medium', 'hard', 'unbeatable']
    if (player_sign not in sign) and (level not in l):
        return render(request, '400.html')
    else:
        return render(request, 'ttt_single_game.html', {'player_sign': player_sign, 'level': level})


@login_required
@api_view(['GET', 'POST'])
def max_score(request):
    if request.method == 'GET':
        try:
            return Response(data={'maxScore': getattr(MaxScore.objects.get(user=request.user), request.GET['level'])}, status=status.HTTP_200_OK)
        except:
            return Response(data={'maxScore': getattr(MaxScore.objects.create(user=request.user), request.GET['level'])}, status=status.HTTP_200_OK)
    else:
        try:
            user_score = MaxScore.objects.get(user=request.user)
            setattr(user_score, request.POST['level'], request.POST['maxScore'])
            user_score.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


def multi_offline(request):
    return render(request, 'ttt_multi_offline.html')
