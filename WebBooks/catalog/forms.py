from django import forms
from datetime import date
from django.forms import ModelForm
from .models import Book

class AuthorsForm(forms.Form):
    first_name = forms.CharField(label="Author's name")
    last_name = forms.CharField(label="Author's surname")
    date_of_birth = forms.DateField(label="Date of birth",
                                    initial=format(date.today()),
                                    widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    date_of_death = forms.DateField(label="Date of birth",
                                    initial=format(date.today()),
                                    widget=forms.widgets.DateInput(attrs={'type': 'date'}))

class BookModelForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'genre', 'language', 'author', 'summary', 'isbn']