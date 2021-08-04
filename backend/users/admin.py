from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_filter = ('first_name', 'email')


admin.site.register(User, UserAdmin)
