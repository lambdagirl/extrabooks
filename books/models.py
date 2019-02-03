from django.db import models
import uuid, os
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from django.utils.text import slugify
import uuid

# Create your models here.
class Category(models.Model): # The Category table name that inherits models.Model
    name = models.CharField(max_length=100) #Like a varchar
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('books:book_list', args =[str(self.slug)])

    def __str__(self):
        return self.name #name to be shown when called


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    # return the whole path to the file
    return os.path.join(str(instance.seller.id), "book_images", filename)


class Book(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add = True)
    description = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character')
    #title, description, category, ISBN, price
    price = models.DecimalField(max_digits=10,decimal_places=2)
    seller = models.ForeignKey(
            get_user_model(),
            on_delete = models.CASCADE,)
    category = models.ForeignKey('Category', related_name='books',
                                on_delete = models.CASCADE,)
    picture = models.ImageField(upload_to = user_directory_path,
                                verbose_name= 'book_pic',
                                default = 'None/no-img.jpg'
                                )
    tags= TaggableManager()

    class Meta:
        ordering = ('-date',)

    def get_absolute_url(self):
        return reverse('books:book_detail', args =[str(self.id)])

    def __str__(self) -> str:
        return self.name
