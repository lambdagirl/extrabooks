from django import forms

class OfferPriceForm(forms.Form):
    offer_total = forms.DecimalField(max_digits=10,decimal_places=2)
