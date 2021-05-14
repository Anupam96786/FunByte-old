from django.shortcuts import render


def index(request):
    return render(request, 'trex_index.html')
