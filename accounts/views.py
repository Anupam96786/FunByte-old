from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Token
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'GET':
            return render(request, 'login.html')
        elif request.method == 'POST':
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                try:
                    return HttpResponseRedirect(request.GET['next'])
                except:
                    return redirect('home')
            else:
                return render(request, 'login.html', {'message': 'Invalid Credentials'})


def user_signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            if User.objects.filter(email=email)[0].is_active:
                return render(request, 'signup.html', {'emessage': 'This email is already registered.', 'username': username,
                    'email': request.POST['email'], 'firstname': request.POST['firstname'], 'lastname': request.POST['lastname']})
            else:
                User.objects.get(email=email).delete()
                user = User.objects.create_user(
                    username=username, password=request.POST['password'], is_active=False,
                    first_name=request.POST['firstname'], last_name=request.POST['lastname'], email=request.POST['email']
                    )
                token = Token.objects.create(user=user, purpose='ua').token
                domain = get_current_site(request).domain
                mail_subject = 'Account Activation'
                mail_body = 'Please click on the link below to activate your account.\nIf it is a mistake then don\'t click on the link.\n{}://{}/accounts/useractivation/{}'.format(request.scheme, domain, token)
                EmailMessage(mail_subject, mail_body, to=[request.POST['email']]).send()
                return render(request, 'account_activation.html', {'email': request.POST['email']})
        elif User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'umessage': 'This username already exists. Try using another username.',
                'username': username, 'email': request.POST['email'],
                'firstname': request.POST['firstname'], 'lastname': request.POST['lastname']})
        else:
            user = User.objects.create_user(
                username=username, password=request.POST['password'], is_active=False,
                first_name=request.POST['firstname'], last_name=request.POST['lastname'], email=request.POST['email']
                )
            token = Token.objects.create(user=user, purpose='ua').token
            domain = get_current_site(request).domain
            mail_subject = 'Account Activation'
            mail_body = 'Please click on the link below to activate your account.\nIf it is a mistake then don\'t click on the link.\nhttps://{}/accounts/useractivation/{}'.format(domain, token)
            EmailMessage(mail_subject, mail_body, to=[request.POST['email']]).send()
            return render(request, 'account_activation.html', {'email': request.POST['email']})


def user_activation(request, token):
    try:
        token = Token.objects.get(token=token)
        if token.purpose == 'ua':
            user = token.user
            user.is_active = True
            user.save()
            token.delete()
            login(request, user)
            return redirect('home')
        else:
            return render(request, '400.html')
    except:
        return render(request, '400.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('home')


def change_password(request):
    if request.method == 'GET':
        return render(request, 'change_password.html')
    if request.method == 'POST':
        user = authenticate(request, username=request.user.username, password=request.POST['old_password'])
        if user is not None:
            user.password = request.POST['new_password']
            user.save()
        else:
            return render(request, 'change_password.html', {'message': 'Please enter correct password'})
