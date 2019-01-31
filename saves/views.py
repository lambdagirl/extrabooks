from django.shortcuts import render
from django.views.generic import ListView
from .models import SavedBooks

# Create your views here.
class SavedBooksView(ListView):
    model = SavedBooks
    template_name = 'saves.html'
