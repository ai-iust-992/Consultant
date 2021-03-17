from django.contrib import admin
from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'avatar', 'first_name', 'last_name', 'phone number']


admin.site.register(UserProfile, UserProfileAdmin)


class LawyerAdmin(admin.ModelAdmin):
    list_display = ['username', 'avatar', 'first_name', 'last_name', 'phone number', 'accepted']


admin.site.register(Lawyer, LawyerAdmin)
