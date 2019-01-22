from django.db import models

from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
# Create your models here.

class Book(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add = True)
    description = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    #title, description, category, ISBN, price
    price = models.PositiveIntegerField()
    seller = models.ForeignKey(
            get_user_model(),
            on_delete = models.CASCADE,)
    picture = models.ImageField(upload_to = 'pic_folder/')

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('books:book_detail', args =[str(self.id)])
