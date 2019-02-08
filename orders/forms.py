import crispy_forms
from .models import Order, Offer
from django import forms

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields =['first_name','last_name', 'email','address','postal_code',
                        'city']


class OfferPriceForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields =['offer_price']
