from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Roles
from .forms import CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ["username", "email", "first_name", "last_name"]

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        (
            "Custom Info",
            {
                "fields": (
                    "company",
                    "birthday",
                    "street",
                    "house_number",
                    "city",
                    "zip_code",
                    "country",
                    "phone_number",
                    "bank_account",
                    "roles",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "company",
                    "birthday",
                    "street",
                    "house_number",
                    "city",
                    "zip_code",
                    "country",
                    "phone_number",
                    "bank_account",
                    "roles",
                ),
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
