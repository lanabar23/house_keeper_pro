from django import forms
from django.forms import fields
from .models import KeeperApps, Actions, Organizations, QueryAnswers, Actives, Notes, Categories, SubCategories, Books, Plans, Periods, FamilyUsers, ActsCategories, ActSubCategories

class AppsForm(forms.ModelForm):
    class Meta:
        model = KeeperApps
        exclude = []

class FamilyUsersForm(forms.ModelForm):
    class Meta:
        model = FamilyUsers
        exclude = []

class ActionsForm(forms.ModelForm):
    class Meta:
        model = Actions
        exclude = []

class ActsCategoriesForm(forms.ModelForm):
    class Meta:
        model = ActsCategories
        exclude = []

class ActSubCategoriesForm(forms.ModelForm):
    class Meta:
        model = ActSubCategories
        exclude = []

class PeriodsForm(forms.ModelForm):
    class Meta:
        model = Periods
        exclude = []

class QAForm(forms.ModelForm):
    class Meta:
        model = QueryAnswers
        fields = ['shortquery', 'appsname', 'is_urgent', 'source', 'status','resansways', ]  # 'fullquery', 'resolvetime', 'resansfact', 'coment', 'querykind', 
        widgets = {
            'is_urgent': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class ActivesForm(forms.ModelForm):
    class Meta:
        model = Actives
        exclude = []
        widgets = {
            'is_fnsknown': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class OrgForm(forms.ModelForm):
    class Meta:
        model = Organizations
        exclude = []

class NoteForm(forms.ModelForm):
    class Meta:
        model = Notes
        exclude = []
        widgets = {
            'is_nesessary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CatForm(forms.ModelForm):
    class Meta:
        model = Categories
        exclude = []

class SubCatForm(forms.ModelForm):
    class Meta:
        model = SubCategories
        exclude = []

class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['book_name', 'tag_name', 'author', 'buydate', 'bookcost', 'kind_of_book', 'is_verified']

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plans
        exclude = []
 