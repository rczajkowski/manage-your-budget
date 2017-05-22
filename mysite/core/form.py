from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from mysite.core.models import *


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','password1', 'password2')


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class FinanceForm(ModelForm):
    class Meta:
        model = Finance
        fields = '__all__'