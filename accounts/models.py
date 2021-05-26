from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4


class Token(models.Model):
    '''
    fp - forgot password
    cp - change password
    mc - mail confirmation
    '''
    token = models.UUIDField(primary_key = True, default = uuid4, editable = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    purpose = models.CharField(max_length=2, blank=False, null=False)
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'purpose')


class Profile(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=False)
    gender = models.CharField(max_length=6, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    show_email = models.BooleanField(default=False)
    facebook = models.CharField(max_length=100, blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    twitter = models.CharField(max_length=100, blank=True, null=True)
    youtube = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.user.username
