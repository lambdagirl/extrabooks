from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView,DeleteView,CreateView
# Create your views here.
from .models import Book
from django.urls import reverse_lazy

class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'


class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'

class BookDeleteView(DeleteView):
    model = Book
    template_name = 'books/book_delete.html'
    success_url = reverse_lazy('books:book_list')

class BookUpdateView(UpdateView):
    model = Book
    fields = ['name', 'description', 'price']
    template_name = 'books/book_edit.html'

class BookCreateView(CreateView):
    model = Book
    fields = ['name', 'description', 'price', 'isbn','seller']
    template_name = 'books/book_new.html'
    success_url = reverse_lazy('books:book_list')
