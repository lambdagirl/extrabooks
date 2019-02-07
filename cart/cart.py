from decimal import Decimal
from django.conf import settings
from books.models import Book
from operator import itemgetter

class Cart(object):
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart: # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, book):
        """
        Add a book to the cart.
        """
        book_pk = str(book.pk)
        if book_pk not in self.cart:
            #because seller might change the price of the book,we store the current price.
            self.cart[book_pk] = {'price': str(book.price)}
        self.save()

    def save(self):
        self.session.modified=True

    def remove(self, book):
        """
        Remove a book from the cart.
        """
        book_pk = str(book.pk)
        if book_pk in self.cart:
            del self.cart[book_pk]
        self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the book from the databases.
        """
        book_pks = self.cart.keys()
        #get the book objects and add them to the cart.
        books = Book.objects.filter(pk__in=book_pks)

        cart = self.cart.copy()
        for book in books:
            cart[str(book.pk)]['book'] = book
            cart[str(book.pk)]['price'] = book.price
            cart[str(book.pk)]['seller'] = book.seller
        for item in cart.values():
            item['price']=Decimal(item['price'])

            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return len(self.cart.values())

    def get_total_price(self):
        '''
        cart_list = []
        for k,v in self.cart.items():
            cart_list.append(v)
        grouper = ['seller']
        key=itemgetter(*str(grouper))
        cart_list.sort(key=key)
        cart_list = [{**dict(zip(grouper, k)), 'price' : sum(Decimal(map(itemgetter('price')),g))} for k,g in groupby(l,key=key)]
        print(cart_list)
        '''
        return sum(Decimal(item['price']) for item in self.cart.values())

    def clear(self):
        #remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def offer_total_price(self, offer_price):
        return offer_price

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
