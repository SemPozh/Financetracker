from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Review


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Подтверждение пароля'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))


class ReviewForm(forms.Form):
    content = forms.CharField(label='Содержание', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Ваш отзыв'}))
    grade = forms.ChoiceField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')), widget=forms.Select(attrs={'class': 'form-select mb-2'}))


class AddFinanceForm(forms.Form):
    title = forms.CharField(label='Название', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название'}))
    money = forms.IntegerField(label="Цена", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена'}))
    date = forms.DateField(label="Дата", widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    description = forms.CharField(label='Описание', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание', 'rows': 2}))


