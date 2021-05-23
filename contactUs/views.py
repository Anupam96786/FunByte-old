from django.shortcuts import redirect, render
from .models import ContactReason
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test


@login_required
def index(request):
    if request.method == 'GET':
        return render(request, 'cu_index.html')
    elif request.method == 'POST':
        ContactReason.objects.create(user=request.user, title=request.POST['title'], description=request.POST['description'])
        return render(request, 'cu_index.html')


@login_required
@user_passes_test(lambda u: u.is_superuser and u.is_staff)
def reports(request):
    if request.method == 'GET':
        return render(request, 'cu_reports.html', {'reports': ContactReason.objects.all()})

