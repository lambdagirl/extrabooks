from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView,DeleteView,CreateView
from .models import Book, Category
from django.urls import reverse_lazy
from users.models import CustomUser
from django.shortcuts import render,redirect
from django.http import Http404,HttpResponseForbidden
from django.shortcuts import get_object_or_404
from taggit.models import Tag
import sys,redis,isbntools
from .forms import BookCreatebyISBNForm,BookCreatebyISBNForm2
from isbnlib import meta
from isbnlib.registry import bibformatters,PROVIDERS
from isbnlib._desc import goo_desc
from isbnlib._cover import cover
from django.conf import settings
from actions.utils import create_action
from django.contrib.messages.views import SuccessMessageMixin
#connect to redis
r = redis.StrictRedis(host=settings.REDIS_HOST,
                        port = settings.REDIS_PORT,
                        db = settings.REDIS_DB)

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


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #increment total book views by 1
        context["total_views"] = r.incr('context.book:{}:views'.format(context['book'].id))
        #increment book ranking by 1
        r.zincrby('book_ranking',context['book'].id,1)
        return context

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

class BookCreateView(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = Book
    fields = ['name', 'description', 'price', 'isbn' ,'picture', 'category']
    template_name = 'books/book_new.html'
    success_url = reverse_lazy('books:book_list')
    login_url = 'login'
    success_message = "%(name)s was created successfully"

    def form_valid(self,form):
        form.instance.seller = self.request.user
        self.object = form.save(commit=False)
        self.object.save()
        print(self.object)
        create_action(self.request.user,'selling a book', self.object)
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data,
                                           calculated_field=self.object.name)


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

def book_ranking(request):
    #get image ranking dectionary
    book_ranking = r.zrange('book_ranking',0,-1, desc = True)[:10]
    book_ranking_ids = [int(id) for id in book_ranking]
    #get most viewed images
    most_viewed = list(Book.objects.filter(id__in=book_ranking_ids))
    most_viewed.sort(key=lambda x: book_ranking_ids.index(x.id))
    return render(request,
                    'books/ranking.html',
                    {'section':'books',
                    'most_viewed':most_viewed})
