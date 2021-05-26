from django.contrib import admin
from .models import MaxScore, UserRoom

@admin.register(MaxScore)
class MaxScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'easy', 'moderate', 'hard', 'unbeatable']


admin.site.register(UserRoom)
