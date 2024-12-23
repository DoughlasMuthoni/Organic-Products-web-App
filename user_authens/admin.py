from django.contrib import admin

# Register your models here.
from user_authens.models import Profile, User

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'bio']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'bio', 'phone']

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)