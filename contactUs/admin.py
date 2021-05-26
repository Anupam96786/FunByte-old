from django.contrib import admin
from .models import ContactReason

@admin.register(ContactReason)
class ContactReasonAdmin(admin.ModelAdmin):
    list_display = ['user', 'title']
