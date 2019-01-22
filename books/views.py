from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView,DeleteView,CreateView
from .models import Book
from django.urls import reverse_lazy
from users.models import CustomUser
from django.shortcuts import render
from django.db.models import Q
#from .forms import ImageUploadForm

from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404


class BookListView(ListView):
    model = Book
    queryset = model.objects.order_by('-date')
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
    fields = ['name', 'description', 'price', 'picture']
    template_name = 'books/book_edit.html'
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj.seller == self.request.user

class BookCreateView(LoginRequiredMixin,CreateView):
    model = Book
    fields = ['name', 'description', 'price', 'isbn' ,'picture']
    template_name = 'books/book_new.html'
    success_url = reverse_lazy('books:book_list')
    login_url = 'login'

    def form_valid(self,form):
        form.instance.seller = self.request.user
        return super().form_valid(form)



def search(request):
    term = request.GET.get('q')
    books = Book.objects.filter(
        Q(name__icontains=term)|Q(description__icontains=term))
    return render(request, 'books/book_list.html', {'book_list':books})
'''
def upload_pic(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            book = Book()
            book.picture = form.cleaned_data['image']
            book.save()
            return HttpResponse('image upload success')

    return HttpResponseForbidden('allowed only via POST')
'''
