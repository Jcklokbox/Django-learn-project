from django import forms
from .models import News
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


class FeedbackForm(forms.Form):
    subject = forms.CharField(label='Тема', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Сообщение', max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    captcha = CaptchaField(label='Проверка на робота')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', max_length=150,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', max_length=150,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Адрес электронной почты', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', max_length=150, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', max_length=150, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'category', 'is_published']
        widgets = {
            'title': forms.TextInput({'class': 'form-control'}),
            'content': forms.Textarea({'class': 'form-control', 'rows': 5}),
            'category': forms.Select({'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if title[0].lower() == title[0]:
            raise ValidationError('Название не должно начинаться c маленькой буквы.')
        return title