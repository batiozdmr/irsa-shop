from django import forms

from apps.accounts.models import Address
from django.contrib.auth.models import Group, User
from allauth.account.forms import ChangePasswordForm


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "name",
            "first_name",
            "last_name",
            "tc",
            "company_name",
            "company_tax",
            "phone",
            "city",
            "street_address_1",
            "billing_address",
            "shipping_address",
        ]

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        for arr in self.fields:
            self.fields[arr].widget.attrs.update({'class': 'form-control ', })


class UserForm(forms.ModelForm):
    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "email",
        ]
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for arr in self.fields:
            self.fields[arr].widget.attrs.update({'class': 'form-control ', })
