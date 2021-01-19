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
            return render(request, 'login.html')


def user_signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'emessage': 'This email is already registered.', 'username': username,
                'email': request.POST['email'], 'firstname': request.POST['firstname'], 'lastname': request.POST['lastname']})
        elif User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'umessage': 'This username already exists. Try using another username.',
                'username': username, 'email': request.POST['email'],
                'firstname': request.POST['firstname'], 'lastname': request.POST['lastname']})
        else:
            user = User.objects.create_user(
                username=username, password=request.POST['password'],
                first_name=request.POST['firstname'], last_name=request.POST['lastname']
                )
            login(request, user)
            token = Token.objects.create(user=user, purpose='ec', email=request.POST['email']).token
            domain = get_current_site(request).domain
            mail_subject = 'Email Confirmation'
            mail_body = 'Please click on the link below to confirm your email address.\nIf it is a mistake then don\'t click on the link.\n{}://{}/accounts/emailconfirmation/{}'.format(request.scheme, domain, token)
            EmailMessage(mail_subject, mail_body, to=[request.POST['email']]).send()
            return redirect('home')


def email_confirmation(request, token):
    try:
        token = Token.objects.get(token=token)
        if token.purpose == 'ec':
            user = token.user
            user.email = token.email
            user.save()
            token.delete()
            login(request, user)
            return redirect('home')
        else:
            return render('400.html')
    except:
        return render('400.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('home')
