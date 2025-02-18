from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from .models import (
    User,
    UserProfile,
)

admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(Permission)
