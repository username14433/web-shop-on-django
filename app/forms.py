from django import forms
from .models import User, Order, BasketProduct


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
    email = forms.EmailField(required=False)
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


class OrderForm(forms.ModelForm, forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    address = forms.CharField(required=True)

    class Meta:
        model = Order
        fields = (
            'first_name',
            'last_name',
            'address',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['address'].label = 'Адрес доставки'
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'

    def clean(self):
        address = self.cleaned_data['address']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']


class HelpForm(forms.Form):
    problem = forms.CharField(required=False)
    question = forms.CharField(required=True)
    username = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['problem'].label = 'Проблема'
        self.fields['question'].label = 'Вопрос'
        self.fields['username'].label = 'Имя пользователя'

    def clean(self):
        username = self.cleaned_data['username']
        question = self.cleaned_data['question']
        problem = self.cleaned_data['problem']
        user = User.objects.filter(username=username)
        if not user.exists():
            raise forms.ValidationError(f'{username} не существует в системе')

# class QuantityForm(forms.ModelForm):
#     quantity = forms.IntegerField(required=True)
#     class Meta:
#         model = BasketProduct
#         fields = (
#             'quantity',
#         )
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['quantity'].label = 'quantity'
#     def clean(self):
#         quantity = self.cleaned_data['quantity']
