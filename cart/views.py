from django.shortcuts import render, redirect, get_object_or_404
from books.models import Book
from .cart import Cart
from .forms import OfferPriceForm
from django.views.decorators.http import require_POST
# Create your views here.
from operator import itemgetter

@require_POST
def cart_add(request,book_pk):
    cart = Cart(request)
    book = get_object_or_404(Book, pk = book_pk)
    cart.add(book=book)
    return redirect('cart:cart_detail')

def cart_remove(request, book_pk):
    cart = Cart(request)
    book = get_object_or_404(Book, pk = book_pk)
    cart.remove(book)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    book_list = []
    for item in cart:
        book_list.append(item)
    seller = [d['seller'].username for d in book_list]
    book_list = sorted(book_list, key=lambda k: k['seller'].username)
    return render(request, 'cart/detail.html', {'cart':cart, 'book_list':book_list, 'seller':seller})
'''
def make_offer(request):
    return render(request, 'cart/offer.html', {})
    '''
