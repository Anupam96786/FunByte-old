from django.db import models
from django.contrib.auth.models import User


class BugReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
