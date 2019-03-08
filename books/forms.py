from django import forms
from .models import Book, BookImage
from django.forms.models import modelformset_factory

class BookCreatebyISBNForm(forms.Form):
    isbn = forms.CharField( max_length=14, help_text='10 or 13 Character')

class BookCreatebyISBNForm2(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('price','category','city', 'condition')

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = BookImage
        fields = ('image', )

ImageFormSet = modelformset_factory(BookImage,form=ImageForm, extra=2)
