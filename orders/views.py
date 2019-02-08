from django.shortcuts import render,redirect
from .forms import OrderCreateForm, OfferPriceForm
from cart.cart import Cart
from books.models import Book
from .models import Offer,OfferItem
from decimal import Decimal

# Create your views here.

def order_create(request,):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = forms.save()

def make_offer(request, seller):
    form = OfferPriceForm(request.GET)
    seller = seller
    cart = Cart(request)
    book_pks = cart.cart.keys()
    books = Book.objects.filter(pk__in=book_pks).filter(seller__username = seller)
    total_price = 0
    for book in books:
        total_price += book.price
        print(book.name)
    if request.method == 'POST':
        form = OfferPriceForm(request.POST)
        if form.is_valid():
            offer_price = form.cleaned_data['offer_price']
            print(offer_price)
            offer = form.save(commit = False)
            offer.user = request.user
            offer.offer_price = offer_price
            offer.save()
            for book in books:
                OfferItem.objects.create(offer = offer,
                                        book = book,
                                        price =book.price)
            #form = OrderCreateForm()
            #return render(request,'orders/offer_created.html',{'offer':offer, 'form':form})
            return redirect('orders:create_order')
        else:
            form =  OfferPriceForm()
    return render(request, 'orders/make_offer.html', {'books':books, 'seller':seller, 'form':form})

def create_order(request):
    form = OrderCreateForm(request.GET)
    return render(request,'orders/offer_created.html',{'form':form})
