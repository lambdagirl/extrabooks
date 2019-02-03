from django import forms
from .models import Book

class BookCreatebyISBNForm(forms.Form):
    isbn = forms.CharField( max_length=13, help_text='13 Character')

class BookCreatebyISBNForm2(forms.Form):
    price = forms.IntegerField()
