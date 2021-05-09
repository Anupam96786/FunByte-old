from django.db import models
from django.contrib.auth.models import User
import uuid


class SMID(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' --> ' + self.user.username


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    def __str__(self):
        return self.message
