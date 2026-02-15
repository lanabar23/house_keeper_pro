from django import forms
from .models import ActionsFacts, BooksFacts, UsersActions

class ActDoneForm(forms.ModelForm):
    class Meta:
        model = ActionsFacts
        exclude = []

class UsersActionsForm(forms.ModelForm):
    class Meta:
        model = UsersActions
        fields = ['actdone', 'actstart']
        labels = {
            'actdone': 'Действие',
            'actstart': 'Время начала',
        }

class BookDoneForm(forms.ModelForm):
    class Meta:
        model = BooksFacts
        exclude = []
