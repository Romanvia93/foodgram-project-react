from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_filter = ('first_name', 'email')


admin.site.register(User, UserAdmin)