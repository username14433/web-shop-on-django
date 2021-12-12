from django import forms
from .models import User


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.filter(username=username)
        if not user.exists():
            raise forms.ValidationError(f'{username} не существует в системе')
        if user:
            if not user.first().check_password(password):
                raise forms.ValidationError('Пароль неверный')
        return self.cleaned_data


class RegistrationForm(forms.ModelForm):
    phone = forms.CharField(required=False)
    email = forms.CharField(required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'phone', 'confirm_password')

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        if user:
            raise forms.ValidationError('Такое имя уже существует!')
        return username
