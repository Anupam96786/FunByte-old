from django.contrib.auth.models import User
from django.db import models
import uuid


class MaxScore(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ttt_user')
    easy = models.IntegerField(default=0)
    moderate = models.IntegerField(default=0)
    hard = models.IntegerField(default=0)
    unbeatable = models.IntegerField(default=0)


class UserRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='main_user')
    connected = models.ManyToManyField(User, related_name='connected_user', blank=True)
    board = models.CharField(max_length=9, default='000000000')
    turn = models.CharField(default='O', max_length=1)
    scoreX = models.IntegerField(default=0)
    scoreO = models.IntegerField(default=0)
