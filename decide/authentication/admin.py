from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.db import models
from .models import Voter

# Register your models here.
class UserProfileInline(admin.TabularInline):
    model = Voter

class UserCustomAdmin(UserAdmin):
    inlines = [UserProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserCustomAdmin)


