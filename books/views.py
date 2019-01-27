from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView,DeleteView,CreateView
from .models import Book, Category
from django.urls import reverse_lazy
from users.models import CustomUser
from django.shortcuts import render
from django.db.models import Q
#from .forms import ImageUploadForm
from django.http import Http404

from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404


class BookListView(ListView):
    model = Book
    queryset = model.objects.order_by('-date')
    select_related = ("seller", "category")
    template_name = 'books/book_list.html'

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

class BookListbyCategoryView(ListView):
    model = Category
    template_name = 'books/explore.html'
'''

    def get_queryset(self, queryset=None):
        pk = self.kwargs.get(self.lookup_url_kwarg)
        if pk is not None:
            queryset = Book.objects.filter(category_pk=pk)
            print(queryset)
        return queryset
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['category'] = (
                self.Category.filter(
                    pk__in=books.category.values_list("category__pk")
                ))
        print("context: ", context)

        return context
'''
def search(request):
    term = request.GET.get('q')
    books = Book.objects.filter(
        Q(name__icontains=term)|Q(description__icontains=term))
    return render(request, 'books/book_list.html', {'book_list':books})
