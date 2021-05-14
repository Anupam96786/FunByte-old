from django.contrib import admin
from .models import MaxScore

@admin.register(MaxScore)
class MaxScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'score']
