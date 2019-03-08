from django.test import TestCase
from django.core.files.images import ImageFile
from .models import BookImage, Book
from decimal import Decimal

# Create your tests here.

class TestSignal(TestCase):
    def test_thumbnails_are_generated_on_save(self):
        book = Book(
            name="The cathedral and the bazaar",
            price=Decimal("10.00")
        )
        book.save()

