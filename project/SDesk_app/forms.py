from django import forms
from django.forms import TextInput, Textarea
from django.contrib.auth import get_user_model
from .models import Task, Profile

class LoginForm(forms.Form):
    username = forms.CharField(label='Пользователь', max_length=30, widget=forms.TextInput(attrs={'class': 'form-input form-label form-control-lg', 'placeholder': 'Логин'}))
    password = forms.CharField(label='Пароль', max_length=30, widget=forms.PasswordInput(attrs={'class': 'form-input form-label form-control-lg', 'placeholder': 'Пароль'}))


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='Логин', max_length=30, widget=forms.TextInput(attrs={'class': 'form-input form-label form-control-lg', 'placeholder': 'Логин'}))
    last_name = forms.CharField(label='Фамилия', max_length=30, widget=forms.TextInput(attrs={'class': 'form-input form-label form-control-lg', 'placeholder': 'Фамилия'}))
    first_name = forms.CharField(label='Имя', max_length=30, widget=forms.TextInput(attrs={'class': 'form-input form-label form-control-lg', 'placeholder': 'Имя'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input form-label form-control-lg', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input form-label form-control-lg', 'placeholder': 'Повтор пароля'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'last_name', 'first_name', 'password', 'password2', ]

    def clean_password2(self):
        pwrd = self.cleaned_data
        if pwrd['password'] != pwrd['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return pwrd['password2']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']

        widgets = {
            'title': TextInput(attrs={'class': 'form-control px-2 my-2',
                                      'placeholder': 'Тема'}),
            'description': Textarea(attrs={'class': 'form-control px-2 my-2',
                                      'placeholder': 'Подробное описание проблемы'})
        }

    def ValidationError(self, param):
        forms.ValidationError('Форма заполнена не верно!')

class ExecUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('executor',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['executor'].queryset = Profile.objects.filter(staff_position__department__short_name='IT')

class CompleteAndRejectUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('answer',)

        widgets = {
            'answer': Textarea(attrs={'class': 'form-control px-2 my-2',
                                      'placeholder': 'Ответ исполнителя инициатору'})
        }