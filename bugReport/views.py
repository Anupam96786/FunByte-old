from django.shortcuts import redirect, render
from .models import BugReport
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'br_index.html', {'reports': BugReport.objects.all().order_by('-id')[0:50]})


@login_required
def report(request):
    if request.method == 'GET':
        return render(request, 'br_report.html')
    elif request.method == 'POST':
        BugReport.objects.create(user=request.user, title=request.POST['title'], description=request.POST['description'])
        return redirect('br_index')

