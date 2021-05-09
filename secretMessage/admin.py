from django.contrib import admin
from .models import Message, SMID

admin.site.register(SMID)
admin.site.register(Message)