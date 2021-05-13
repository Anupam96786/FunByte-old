from django.contrib.auth.models import User
from django.db import models


class MaxScore(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    easy = models.IntegerField(default=0)
    moderate = models.IntegerField(default=0)
    hard = models.IntegerField(default=0)
    unbeatable = models.IntegerField(default=0)
