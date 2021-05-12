from django.shortcuts import render


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


def multi_offline(request):
    return render(request, 'ttt_multi_offline.html')
