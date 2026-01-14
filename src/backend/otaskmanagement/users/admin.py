"""Admin class definitions for the 'user' app."""

from django.contrib import admin
from .models import CustomUser as User


# Register your models here.
class ManageUser(admin.ModelAdmin):
    pass


admin.site.register(User, ManageUser)
