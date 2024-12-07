from django.contrib import admin

# Register your models here.
from user_authens.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'bio']
admin.site.register(User, UserAdmin)