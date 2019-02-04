from django.shortcuts import render
from .models import OfferBook
from .forms import OrderCreateForm
# Create your views here.

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = forms.save()
            
