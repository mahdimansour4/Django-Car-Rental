from django import forms
from .models import Car, User, Payment , Review
import re
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['name', 'model', 'year', 'price', 'image', 'city']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'})
        }

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method', 'card_number', 'card_holder', 'expiry_date', 'cvv']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'card_number': forms.TextInput(attrs={'class': 'form-control'}),
            'card_holder': forms.TextInput(attrs={'class': 'form-control'}),
            'expiry_date': forms.TextInput(attrs={'class': 'form-control'}),
            'cvv': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number').replace(' ', '')
        if not card_number.isdigit() or len(card_number) != 16:
            raise forms.ValidationError('Card number must be 16 digits.')
        return card_number

    def clean_expiry_date(self):
        expiry_date = self.cleaned_data.get('expiry_date')
        if not re.match(r'^\d{2}/\d{2}$', expiry_date):
            raise forms.ValidationError('Expiry date must be in MM/YY format.')
        return expiry_date

    def clean_cvv(self):
        cvv = self.cleaned_data.get('cvv')
        if not cvv.isdigit() or len(cvv) != 3:
            raise forms.ValidationError('CVV must be 3 digits.')
        return cvv



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }