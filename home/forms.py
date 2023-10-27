from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Roles
from django import forms


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "input-group-text"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "input-group-text"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "input-group-text"}))
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            'email',
            'first_name',
            'last_name',
            'company',
            'birthday',
            'street',
            'house_number',
            'city',
            'zip_code',
            'country',
            'phone_number',
            'bank_account',
        )

        widgets = {
            'email': forms.EmailInput(attrs={"class": "input-group-text"}),
            'first_name': forms.TextInput(attrs={"class": "input-group-text"}),
            'last_name': forms.TextInput(attrs={"class": "input-group-text"}),
            'company': forms.TextInput(attrs={"class": "input-group-text"}),
            'birthday': forms.DateInput(attrs={"class": "input-group-text"}),
            'street': forms.TextInput(attrs={"class": "input-group-text"}),
            'house_number': forms.TextInput(attrs={"class": "input-group-text"}),
            'city': forms.TextInput(attrs={"class": "input-group-text"}),
            'zip_code': forms.TextInput(attrs={"class": "input-group-text"}),
            'country': forms.TextInput(attrs={"class": "input-group-text"}),
            'phone_number': forms.TextInput(attrs={"class": "input-group-text"}),
            'bank_account': forms.TextInput(attrs={"class": "input-group-text"}),
        }

        def __init__(self) -> None:
            super(CustomUserCreationForm, self).__init__(*args, **kwargs)
            self.fields['username'].widget.attrs.update({'class': 'input-group-text'})
            self.fields['password1'].widget.attrs.update({'class': 'input-group-text'})
            self.fields['password2'].widget.attrs.update({'class': 'input-group-text'})
            self.fields['email'].widget.attrs.update({'class': 'input-group-text'})
            self.fields['first_name'].widget.attrs.update({'class': 'input-group-text'})
            self.fields['last_name'].widget.attrs.update({'class': 'input-group-text'})
            self.fields['company'].widget.attrs.update({'class': 'input-group-text'})
            self.fields['birthday'].widget.attrs.update({'class': 'input-group-text'})
            self.fields['street'].widget.attrs.update({'class': 'input-group-text'})
            self.fields['house_number'].widget.attrs.update({'class': 'input-group-text'})
            self.fields['city'].widget.attrs.update({'class': 'input-group-text'})
            self.fields['zip_code'].widget.attrs.update({'class': 'input-group-text'})
            self.fields['country'].widget.attrs.update({'class': 'input-group-text'})
            self.fields['phone_number'].widget.attrs.update({'class': 'input-group-text'})
            self.fields['bank_account'].widget.attrs.update({'class': 'input-group-text'})
                                                            

class RoleForm(forms.ModelForm):
    class Meta:
        model = Roles
        fields = (
            'name',
            'description',
        )
        widgets = {
            'name': forms.TextInput(attrs={"class": "input-group-text"}),
            'description': forms.TextInput(attrs={"class": "input-group-text"}),
        }
        def __init__(self) -> None:
            super(RoleForm, self).__init__(*args, **kwargs)
            self.fields['name'].widget.attrs.update({'class': 'input-group-text'})
            self.fields['description'].widget.attrs.update({'class': 'input-group-text'})
                                