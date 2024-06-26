from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from predictionGame.users.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email')

    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)