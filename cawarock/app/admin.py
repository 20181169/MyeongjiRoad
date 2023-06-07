from django.contrib import admin
from rest_framework_api_key.admin import APIKeyModelAdmin
from rest_framework_api_key.models import APIKey

from django.contrib import admin
from .models import MyUser
from django.contrib.auth.admin import UserAdmin
from .models import Account, Market_DB


from .models import Market_DB, Images, review, Account

class ImagesInline(admin.TabularInline):
    model = Images

class reviewInline(admin.TabularInline):
    model = review



class MarketDBAdmin(admin.ModelAdmin):
    inlines = [ImagesInline, reviewInline]
    readonly_fields = ['display_images']

    def display_images(self, obj):
        images = obj.images.all()
        if images:
            return ', '.join([str(image) for image in images])
        else:
            return 'No images'

    display_images.short_description = 'Images'

class accountAdmin(admin.ModelAdmin):
    inlines = [reviewInline]
    

admin.site.register(Market_DB, MarketDBAdmin)

admin.site.register(Account, accountAdmin)

admin.site.register(Images)

admin.site.register(review)

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
