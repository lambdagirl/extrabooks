from django.db import models
from books.models import Book
from django.contrib.auth import get_user_model
# Create your models here.

class Offer(models.Model):
    user = models.ForeignKey(
                get_user_model(),
                on_delete = models.CASCADE,)
    offer_price = models.DecimalField(max_digits=10,decimal_places=2)

    def get_total_cost():
        return sum(item.get_cost() for item in self.items.all())

class OfferItem(models.Model):
    offer = models.ForeignKey(Offer, related_name='items', on_delete = models.CASCADE,)
    book = models.ForeignKey(
                Book,
                related_name='offer_items',
                on_delete = models.CASCADE,)
    price = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price

class Order(models.Model):
    offer = models.OneToOneField(
        Offer,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=120)
    postal_code = models.CharField(max_length=20)
    city=models.CharField(max_length=100)
    created =models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=150,blank = True)

    class Meta:
        ordering = ('-created',)
