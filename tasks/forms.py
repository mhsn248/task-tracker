from django import forms
from .models import Task


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

            'started_at': forms.DateInput(

                attrs={

                    'class': 'form-control',

                    'type': 'date',

                }

            ),

        }
