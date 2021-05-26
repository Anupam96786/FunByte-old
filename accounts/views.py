from time import time
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Token, Profile
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
import datetime


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
        if email:
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
                Profile.objects.create(user=user, email=request.POST['email'])
                token = Token.objects.create(user=user, purpose='mc').token
                domain = get_current_site(request).domain
                mail_subject = 'Mail Confirmation'
                mail_body = 'Please click on the link below to confirm your email id.\nIf it is a mistake then don\'t click on the link.\nhttps://{}/accounts/mailconfirmation/{}'.format(domain, token)
                EmailMessage(mail_subject, mail_body, to=[request.POST['email']]).send()
                login(request, user)
                return redirect('home')
        elif User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'umessage': 'This username already exists. Try using another username.',
                'username': username, 'email': request.POST['email'],
                'firstname': request.POST['firstname'], 'lastname': request.POST['lastname']})
        else:
            user = User.objects.create_user(
                username=username, password=request.POST['password'],
                first_name=request.POST['firstname'], last_name=request.POST['lastname']
                )
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('home')


def mail_confirmation(request, token):
    try:
        token = Token.objects.get(token=token)
        if token.purpose == 'mc':
            user = token.user
            user.email = Profile.objects.get(user=user).email
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


@login_required
def change_password(request):
    if request.method == 'GET':
        return render(request, 'change_password.html')
    if request.method == 'POST':
        user = authenticate(request, username=request.user.username, password=request.POST['old_password'])
        if user is not None:
            user.set_password(request.POST['new_password'])
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'change_password.html', {'message': 'Please enter correct password'})


def forgot_password(request):
    if request.method == 'GET':
        return render(request, 'forgot_password.html')
    if request.method == 'POST':
        try:
            user = User.objects.get(email=request.POST['email'])
            token = Token.objects.get_or_create(user=user, purpose='fp')[0].token
            domain = get_current_site(request).domain
            mail_subject = 'Change Password'
            mail_body = 'Please click on the link below to change your password.\nIf it is a mistake then don\'t click on the link.\nhttps://{}/accounts/fpchange/{}'.format(domain, token)
            EmailMessage(mail_subject, mail_body, to=[request.POST['email']]).send()
            return render(request, 'fp_email_sent.html', {'email': request.POST['email']})
        except:
            return render(request, 'forgot_password.html', {'message': 'Not a registered email'})


def fp_change(request, token):
    if request.method == 'GET':
        return render(request, 'fp_change.html')
    if request.method == 'POST':
        try:
            token = Token.objects.get(token=token)
            if token.purpose == 'fp':
                user = token.user
                user.set_password(request.POST['password'])
                user.save()
                token.delete()
                login(request, user)
                return redirect('home')
            else:
                return render(request, '400.html')
        except:
            return render(request, '400.html')


def profile(request, username):
    if request.method == 'GET':
        return render(request, 'profile.html', {'user': User.objects.get(username=username)})


@login_required
def edit_profile(request):
    if request.method == 'GET':
        days_left = request.user.date_joined.date() + datetime.timedelta(days=30) - datetime.date.today()
        days_left = days_left.days
        return render(request, 'edit_profile.html', {'days_left': days_left})
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        try:
            if request.POST['show_email'] == 'on':
                user.profile.show_email = True
        except:
            user.profile.show_email = False
        user.profile.gender = request.POST['gender']
        user.profile.about = request.POST['about']
        user.profile.website = request.POST['website']
        user.profile.facebook = request.POST['facebook']
        user.profile.instagram = request.POST['instagram']
        user.profile.twitter = request.POST['twitter']
        user.profile.youtube = request.POST['youtube']
        if request.POST['email'] and user.profile.email != request.POST['email']:
            user.email = ''
            user.profile.email = request.POST['email']
            token = Token.objects.get_or_create(user=request.user, purpose='mc')[0].token
            domain = get_current_site(request).domain
            mail_subject = 'Mail Confirmation'
            mail_body = 'Please click on the link below to confirm your email id.\nIf it is a mistake then don\'t click on the link.\nhttps://{}/accounts/mailconfirmation/{}'.format(domain, token)
            EmailMessage(mail_subject, mail_body, to=[request.user.profile.email]).send()
        elif not request.POST['email']:
            user.email = ''
            user.profile.email = request.POST['email']
        user.save()
        user.profile.save()
        return redirect('edit_profile')


def get_verification_link(request):
    if request.method == 'GET' and not request.user.email:
        token = Token.objects.get_or_create(user=request.user, purpose='mc')[0].token
        domain = get_current_site(request).domain
        mail_subject = 'Mail Confirmation'
        mail_body = 'Please click on the link below to confirm your email id.\nIf it is a mistake then don\'t click on the link.\nhttps://{}/accounts/mailconfirmation/{}'.format(domain, token)
        EmailMessage(mail_subject, mail_body, to=[request.user.profile.email]).send()
        return render(request, 'mail_verification.html', {'email': request.user.profile.email})
