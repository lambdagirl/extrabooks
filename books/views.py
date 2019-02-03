from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView,DeleteView,CreateView
from .models import Book, Category
from django.urls import reverse_lazy
from users.models import CustomUser
from django.shortcuts import render,redirect
from django.db.models import Q
#from .forms import ImageUploadForm
from django.http import Http404,HttpResponseForbidden
from django.shortcuts import get_object_or_404
from taggit.models import Tag
import sys
import isbntools
from .forms import BookCreatebyISBNForm,BookCreatebyISBNForm2
from isbnlib import meta
from isbnlib.registry import bibformatters,PROVIDERS
from isbnlib._desc import goo_desc
from isbnlib._cover import cover

class BookListView(ListView):
    model = Book
    tag = None
    queryset = model.objects.order_by('-date')
    select_related = ("seller", "category")
    template_name = 'books/book_list.html'

def book_list_by_tag(request,tag_slug=None):
    tag = None
    print(tag_slug)
    tag = get_object_or_404(Tag, slug=tag_slug)
    book_list = Book.objects.filter(tags__in=[tag])
    return render(request, 'books/book_list.html', {'book_list':book_list,
                                                'tag':tag})

def book_list_category(request,category_slug=None):
    category = None
    print(category_slug)
    category= get_object_or_404(Category,slug=category_slug)
    book_list = Book.objects.filter(category__in=[category])
    return render(request, 'books/categories.html', {'book_list':book_list,
                                                'category':category})

class MyBookListView(ListView):
    model = Book
    template_name = 'books/my_book_list.html'

    def get_queryset(self):
        u = CustomUser.objects.get(username=self.request.user)
        return Book.objects.filter(seller=u)

class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'

class BookDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'books/book_delete.html'
    success_url = reverse_lazy('books:book_list')
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj.seller == self.request.user

class BookUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Book
    fields = ['name', 'description', 'price', 'picture', 'category']
    template_name = 'books/book_edit.html'
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj.seller == self.request.user

class BookCreateView(LoginRequiredMixin,CreateView):
    model = Book
    fields = ['name', 'description', 'price', 'isbn' ,'picture', 'category']
    template_name = 'books/book_new.html'
    success_url = reverse_lazy('books:book_list')
    login_url = 'login'

    def form_valid(self,form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

def book_create_by_ISBN(request):
    if request.method == 'POST':
        form = BookCreatebyISBNForm(data=request.POST)
        if form.is_valid():
            isbn = form.cleaned_data['isbn']
            print(isbn)
            name = (meta(isbn)['Title'])
            picture = (cover(isbn)['thumbnail'])
            description = (goo_desc(isbn))
        return render(request,'books/book_new2.html',{'isbn':isbn,
                                                        'name':name,
                                                        'picture':picture,
                                                        'description':description})
    else:
        form = BookCreatebyISBNForm(data=request.GET)
    return render(request,'books/book_new_by_ISBN.html',{'form':form})

def book_create_by_ISBN_2(request):
    if request.method == 'POST':
        return render(request,'books/book_new2.html')


class BookListbyCategoryView(ListView):
    model = Category
    template_name = 'books/categories.html'


def search(request):
    term = request.GET.get('q')
    books = Book.objects.filter(
        Q(name__icontains=term)|Q(description__icontains=term))
    return render(request, 'books/book_list.html', {'book_list':books})
