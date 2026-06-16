from .models import Task
from django.contrib.auth.models import User
from django import forms


class TaskForm(forms.ModelForm):

    class Meta:

        model = Task

        fields = [
            'title',
            'started_at',
        ]

        widgets = {

            'title': forms.TextInput(

                attrs={

                    'class': 'form-control',

                    'placeholder':
                        'مثلا: خواندن قرآن',

                    'autocomplete': 'off',

                    'autofocus': True,

                }

            ),

            'started_at': forms.HiddenInput(),

        }


class RegisterForm(forms.Form):

    username = forms.CharField(

        label='نام کاربری',

        max_length=150,

        widget=forms.TextInput(

            attrs={

                'class': 'form-control',

                'placeholder': 'نام کاربری',

                'autocomplete': 'off',

                'autofocus': True,

            }

        ),

    )

    password1 = forms.CharField(

        label='رمز عبور',

        widget=forms.PasswordInput(

            attrs={

                'class': 'form-control',

                'placeholder': 'رمز عبور',

            }

        ),

    )

    password2 = forms.CharField(

        label='تکرار رمز عبور',

        widget=forms.PasswordInput(

            attrs={

                'class': 'form-control',

                'placeholder': 'تکرار رمز عبور',

            }

        ),

    )

    def clean_username(self):

        username = self.cleaned_data['username']

        if User.objects.filter(
            username=username
        ).exists():

            raise forms.ValidationError(
                'این نام کاربری قبلاً ثبت شده است.'
            )

        return username

    def clean(self):

        cleaned_data = super().clean()

        password1 = cleaned_data.get(
            'password1'
        )

        password2 = cleaned_data.get(
            'password2'
        )

        if (
            password1
            and password2
            and password1 != password2
        ):

            raise forms.ValidationError(
                'رمزهای عبور یکسان نیستند.'
            )

        return cleaned_data

    def save(self):

        user = User.objects.create_user(

            username=self.cleaned_data[
                'username'
            ],

            password=self.cleaned_data[
                'password1'
            ],

        )

        return user
