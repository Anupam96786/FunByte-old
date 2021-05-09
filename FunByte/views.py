from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def error_400(request, exception):
    return render(request,'400.html')


def error_403(request, exception):
    return render(request,'403.html')


def error_404(request, exception):
    return render(request,'404.html')


def error_500(request):
    return render(request,'500.html')
