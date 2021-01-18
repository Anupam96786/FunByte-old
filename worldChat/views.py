from django.shortcuts import render


def index(request):
    return render(request, 'wc_index.html')


def chat(request):
    return render(request, 'wc_chat.html')
