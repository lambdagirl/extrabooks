from django import forms
from .models import Book
class BookCreatebyISBNForm(forms.Form):
    isbn = forms.CharField( max_length=14, help_text='10 or 13 Character')

class BookCreatebyISBNForm2(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('price','category','city', 'condition')
