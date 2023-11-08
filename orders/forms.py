from django import forms
from django.core.exceptions import ValidationError
from home.models import CustomUser, Roles
from .models import (
    Restaurant,
    Location,
)  # , Product, Count, OrderMethod, Orders, PriceHistory, Product_supplier, ProdCategory, SupplierLocation, Supplier


class RestaurantForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(RestaurantForm, self).__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Restaurant
        fields = [
            "name",
            "street",
            "city",
            "house_number",
            "zip_code",
            "country",
            "phone_number",
            "email",
            "website",
            # "user",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "street": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "city": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "house_number": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "zip_code": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "country": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "email": forms.EmailInput(attrs={"class": "form-control mb-5"}),
            "website": forms.TextInput(attrs={"class": "form-control mb-5"}),
        }

        def save(self, commit=True):
            instance = super(RestaurantForm, self).save(commit=False)
            instance.user = self.user
            if commit:
                instance.save()
            return instance


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = [
            "name",
            "street",
            "city",
            "house_number",
            "zip_code",
            "country",
            "phone_number",
            "email",
            "opening_hours",
            "restaurant_id",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "street": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "city": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "house_number": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "zip_code": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "country": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "email": forms.EmailInput(attrs={"class": "form-control mb-5"}),
            "opening_hours": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "restaurant_id": forms.Select(attrs={"class": "form-control mb-5"}),
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["restaurant_id"].queryset = Restaurant.objects.filter(user=user)
