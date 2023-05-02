from django.contrib import admin
from rest_framework_api_key.admin import APIKeyModelAdmin
from rest_framework_api_key.models import APIKey

from django.contrib import admin
from .models import MyUser
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(APIKey)



class MyUserAdmin(UserAdmin):
    model = MyUser
    list_display = ('email', 'username', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(MyUser, MyUserAdmin)

from django.contrib import admin
from rest_framework_api_key.models import APIKey

admin.site.register(APIKey)

from .models import CultureBank

admin.site.register(CultureBank)