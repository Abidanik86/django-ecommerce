from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "phone", "user_type", "is_active", "is_deleted")
    list_filter = ("user_type", "is_active", "is_deleted")
    fieldsets = (
        (None, {"fields": ("username", "email", "phone", "password")}),
        ("Personal Info", {"fields": ("address",)}),
        ("Permissions", {"fields": ("is_active", "is_deleted", "user_type", "is_staff", "is_superuser")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "phone", "password1", "password2", "user_type"),
            },
        ),
    )
    search_fields = ("username", "email", "phone")
    ordering = ("email",)

admin.site.register(CustomUser, CustomUserAdmin)
