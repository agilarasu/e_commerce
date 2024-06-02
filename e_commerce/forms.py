from django import forms
from .models import Product, Profile
from django.contrib.auth.forms import UserCreationForm

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
    password2 = None  # Remove password confirmation field

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('password1',)

    def clean_password2(self):
        return self.cleaned_data.get('password1')  # Skip password validation checks
class ProductFilterForm(forms.Form):
    min_price = forms.DecimalField(required=False)
    max_price = forms.DecimalField(required=False)
    brand = forms.ModelChoiceField(queryset=Product.objects.values_list('brand', flat=True).distinct(), required=False)


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'phone_number']