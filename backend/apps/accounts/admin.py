from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
)

# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ("id","email","phone_number","first_name","last_name","is_active",
        "is_staff","is_email_verified","is_phone_verified","date_joined",)
    list_filter = ("is_active","is_staff","is_superuser","is_email_verified",
        "is_phone_verified",)
    search_fields = ("email","phone_number","first_name","last_name",)
    ordering = ("-date_joined",)
    readonly_fields = ("last_login","date_joined","updated_at",)
    filter_horizontal = ("groups","user_permissions",)
    fieldsets = (
        ("Authentication",{"fields": ("email","phone_number","password",),},),
        ("Personal Information",{"fields": ("first_name","last_name",),},),
        ("Verification",{"fields": ("is_email_verified","is_phone_verified",),},),
        ("Permissions",
            {"fields": ("is_active","is_staff","is_superuser","groups","user_permissions",),},),
        ("Important Dates",{"fields": ("last_login","date_joined","updated_at",),},),
    )
    
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email","phone_number","first_name","last_name","password1","password2",),
            },
        ),
    )