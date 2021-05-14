from django.db import models
from django.contrib.auth.models import User


class MaxScore(models.Model):
    id = models.AutoField(primary_key=True, )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trex_user')
    score = models.IntegerField(default=0)
    def __str__(self) -> str:
        return self.user.username + ' --> ' + str(self.score)
