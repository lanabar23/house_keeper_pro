from django import forms
from .models import FamilyLibrary

class BookForm(forms.ModelForm):
    class Meta:
        model = FamilyLibrary
        fields = ['book_name', 'tag_name', 'kind_of_book', 'author', 'pages', 'subject', 'publ_seria','is_q_and_exc','is_answers','timestart', 'timefin_plan', 'timefin_fact', 'rating','basic_thoughts', 'publ_year','publ_house','publ_city', 'coment']
        widgets = {
            'is_q_and_exc': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_answers': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
