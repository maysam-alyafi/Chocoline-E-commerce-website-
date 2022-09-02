from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email


class CheckoutForm(forms.ModelForm):
    ordered_by = forms.CharField(widget=forms.TextInput(attrs={'required': 'true', 'class': 'form-control'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'required': 'true', 'class': 'form-control'}),
                            validators=[validate_email])
    mobile = forms.CharField(widget=forms.TextInput(attrs={'required': 'true', 'class': 'form-control'}))
    shipping_address = forms.CharField(widget=forms.TextInput(attrs={'required': 'true', 'class': 'form-control'}))

    class Meta:
        model = Order
        fields = ["ordered_by", "shipping_address",
                  "mobile", "email"]

    # function to check mobile number validation
    def clean_mobile(self):
        # get the mobile number
        mobile = self.cleaned_data.get("mobile")
        # check if mobile number is of 10 digits or not and starts with 05 or not
        if len(mobile) != 10:
            raise forms.ValidationError(
                "Mobile number has to be of 10 digits")
        if not mobile.startswith('05'):
            raise forms.ValidationError(
                "Mobile number has to start with 05")

        return mobile

    def clean_ordered_by(self):
        # get the full name from the form
        ordered_by = self.cleaned_data.get("ordered_by")
        # go through each charactr in full name and see if it's digit or not
        if any(char.isdigit() for char in ordered_by):
            raise forms.ValidationError(
                "ordered by cannot contain numbers")

        return ordered_by


class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'required': 'true', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': 'true', 'class': 'form-control'}),
                               validators=[validate_password])
    email = forms.CharField(widget=forms.EmailInput(attrs={'required': 'true', 'class': 'form-control'}),
                            validators=[validate_email])
    address = forms.CharField(widget=forms.TextInput(attrs={'required': 'true', 'class': 'form-control'}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={'required': 'true', 'class': 'form-control'}))

    class Meta:
        model = Customer
        fields = ["username", "password", "email", "full_name", "address"]

    def clean_username(self):
        uname = self.cleaned_data.get("username")

        print(self.cleaned_data)
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError(
                "Customer with this username already exists.")

        return uname

    # function to check if full name contains number or not
    def clean_full_name(self):
        # get the full name from the form
        full_name = self.cleaned_data.get("full_name")
        # go through each charactr in full name and see if it's digit or not
        if any(char.isdigit() for char in full_name):
            raise forms.ValidationError(
                "Full Name cannot contain numbers")

        return full_name


class customerloginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'required': 'true', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': 'true', 'class': 'form-control'}))







class goodForm(forms.ModelForm):
    class Meta:
        model = goods
        fields = ["name", "category", "image", "price", "currency"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the product name here..."
            }),
            "category": forms.Select(attrs={
                "class": "form-control"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "price of the product..."
            }),
            "currency": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "currency of the product..."
            }),
        }
