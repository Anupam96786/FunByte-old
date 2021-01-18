from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4


class Token(models.Model):
    token = models.UUIDField(primary_key = True, default = uuid4, editable = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    purpose = models.CharField(max_length=2, blank=False, null=False)
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'purpose')
