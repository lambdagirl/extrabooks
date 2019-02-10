from django.shortcuts import render,redirect,get_object_or_404
from .tasks import order_created
from .forms import OrderCreateForm, OfferPriceForm
from cart.cart import Cart
from books.models import Book
from .models import Offer,OfferItem, Order
from decimal import Decimal
from django.urls import reverse
# Create your views here.
from django.contrib.sessions.models import Session

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
    if request.method == 'POST':
        form = OfferPriceForm(request.POST)
        if form.is_valid():
            offer_price = form.cleaned_data['offer_price']
            offer = form.save(commit = False)
            offer.user = request.user
            offer.offer_price = offer_price
            offer.save()
            for book in books:
                OfferItem.objects.create(offer = offer,
                                        book = book,
                                        price =book.price)
            request.session['offer_id'] =offer.id
            for book in books:
                cart.remove(book)
            return redirect('orders:create_order')
        else:
            form =  OfferPriceForm()
    return render(request, 'orders/make_offer.html', {'books':books, 'seller':seller, 'form':form})

def create_order(request):
    offer_id =request.session['offer_id']
    form = OrderCreateForm(request.GET)
    offer = get_object_or_404(Offer, pk=offer_id)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            postal_code = form.cleaned_data['postal_code']
            city = form.cleaned_data['city']
            Order.objects.create(offer= offer,
                                first_name = first_name,
                                last_name =last_name,
                                email =email,
                                address = address,
                                postal_code = postal_code,
                                city = city,
                                )
            order_created.delay(offer_id)
            return redirect(reverse('payment:process'))
        else:
            form = OrderCreateForm()
    return render(request,'orders/create_order.html',{'form':form})
