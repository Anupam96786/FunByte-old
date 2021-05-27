from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import MaxScore, UserRoom


def index(request):
    return render(request, 'ttt_index.html')


def single_options(request):
    return render(request, 'ttt_single_options.html')


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
        return Response(data={'maxScore': getattr(MaxScore.objects.get_or_create(user=request.user)[0], request.GET['level'])}, status=status.HTTP_200_OK)
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


def leader_board(request):
    return render(request, 'ttt_leader_board.html')


@api_view(['GET'])
def leader_board_score(request):
    db = MaxScore.objects.order_by(
        "-{}".format(request.GET['level'])
        ).values('user__username', request.GET['level'])
    if request.user.is_authenticated:
        try:
            userScore = MaxScore.objects.filter(user=request.user).values(
                'user__username', request.GET['level']
                )[0]
            return Response(data={
                'data': db[0:50],
                'userData': userScore,
                'userRank': list(db).index(userScore) + 1
            }, status=status.HTTP_200_OK)
        except:
            return Response(data={
                'data': db[0:50],
                'userData': {},
                'userRank': None
            }, status=status.HTTP_200_OK)
    else:
        return Response(data={
            'data': db[0:50],
            'userData': {},
            'userRank': None
        }, status=status.HTTP_200_OK)


def leader_board_user(request, username, level):
    db = MaxScore.objects.order_by('-{}'.format(level)).values('user__username', level)
    user = db.filter(user__username=username)[0]
    return render(request, 'ttt_leaderboard_user.html', {'rank': list(db).index(user) + 1, 'username': username, 'score': user[level]})


@login_required
def multi_online(request):
    room = UserRoom.objects.get_or_create(user=request.user)
    return render(request, 'ttt_multi_online.html', {'roomId': room[0].id, 'roomUser': room[0].user, 'mainBoard': room[0].board, 'turn': room[0].turn, 'scoreX': room[0].scoreX, 'scoreO': room[0].scoreO})


@login_required
def multi_online_id(request, roomId):
    room = UserRoom.objects.get(id=roomId)
    if room.user == request.user:
        return redirect('ttt_multi_online')
    else:
        return render(request, 'ttt_multi_online.html', {'roomId': room.id, 'roomUser': room.user, 'mainBoard': room.board, 'turn': room.turn, 'scoreX': room.scoreX, 'scoreO': room.scoreO})
