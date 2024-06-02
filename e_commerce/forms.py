from .models import Product, Profile, Order
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
"""class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        error_messages = {
            'username': {
                'max_length': "This username is too long.",
            },
            'password2': {
                'password_mismatch': "The two password fields didn’t match.",
            },
        }"""

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username:'
        self.fields['username'].help_text = None
        self.fields['password1'].label = 'Password:'
        self.fields['password1'].help_text = None
        self.fields['password2'].label = 'Password confirmation:'
        self.fields['password2'].help_text = None

        # Override the error messages (optional)
        # self.fields['username'].error_messages = {'required': 'Username is required.'}
        # self.fields['password1'].error_messages = {'required': 'Password is required.'}
        # self.fields['password2'].error_messages = {'required': 'Password confirmation is required.'}

    def save(self, commit=True):
        user = super().save(commit=False)
        # Your additional logic here (e.g., saving user data)
        if commit:
            user.save()
        return user
class ProductFilterForm(forms.Form):
    min_price = forms.DecimalField(required=False)
    max_price = forms.DecimalField(required=False)
    brand = forms.ModelChoiceField(queryset=Product.objects.values_list('brand', flat=True).distinct(), required=False)


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'phone_number']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'payment_method', 'coupon']