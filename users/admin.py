from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.gis.admin import OSMGeoAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, Contact


class CustomUserAdmin(OSMGeoAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'zip_code', 'is_staff','avatar','slug','city','location']

admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Contact)
