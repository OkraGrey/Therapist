from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "gender",
        "age",
        "country",
        "is_verified",
        "is_staff",
    )
    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {"fields": ("gender", "age", "country", "is_verified", "date_verified")},
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("gender", "age", "country")}),
    )
