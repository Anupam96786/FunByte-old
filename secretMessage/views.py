from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from .models import Message, SMID
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@login_required
def index(request):
    user_id = SMID.objects.filter(user=request.user)
    if user_id:
        user_id = user_id[0]
    else:
        user_id = SMID.objects.create(user=request.user)
    return render(request, 'sm_index.html', {
        'domain': get_current_site(request).domain,
        'id': user_id.id,
        'messages': reversed(Message.objects.filter(receiver=user_id.user))
        })


def send_msg(request, user_id):
    if request.method == 'GET':
        try:
            user = SMID.objects.get(id=user_id).user
            if request.user.is_authenticated and request.user == user:
                return redirect('secret_message')
            return render(request, 'sm_send.html')
        except:
            return render(request, '400.html')
    if request.method == 'POST':
        Message.objects.create(receiver=SMID.objects.get(id=user_id).user, message=request.POST['message'])
        return redirect('/')


@api_view(['POST'])
def del_msg(request):
    try:
        Message.objects.get(id=request.data['id']).delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
