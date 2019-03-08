from django.db import models
import uuid, os
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from django.utils.text import slugify
from geopy import distance
from django.contrib.gis.db.models import PointField
from .location import get_city_location

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
    return os.path.join( "book_images", filename)
def user_directory_path2(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    # return the whole path to the file
    return os.path.join( "book_thumbnail", filename)

class Book(models.Model):
    rating = models.DecimalField(max_digits=3,decimal_places=2, default=0,null = True)
    rating_counts = models.PositiveIntegerField( default=0, null = True)
    name = models.CharField(max_length=100, verbose_name= "Title")
    date = models.DateTimeField(auto_now_add = True)
    description = models.TextField(max_length=1000,help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=14, help_text='13 Character')
    price = models.DecimalField(max_digits=10,decimal_places=2, verbose_name= "price")
    tags= TaggableManager(blank=True)
    city = models.CharField(max_length=50,  verbose_name= "city")
    location = PointField(null=True,blank=True)
    picture = models.ImageField(upload_to = user_directory_path,
                                verbose_name= 'book_pic',
                                default = 'None/no-img.jpg')
    seller = models.ForeignKey(
            get_user_model(),
            on_delete = models.CASCADE,)
    category = models.ForeignKey('Category', related_name='books',
                                on_delete = models.CASCADE,  verbose_name= "category")
    CONDITION_CHOICES = (
    ('1', 'New(never used)'),
    ('2', 'Used(like new)'),
    ('3', 'Used(good)'),
    ('3', 'Used(acceptable)'),
    ('4', 'Others'),
)
    condition = models.CharField(max_length=1, choices=CONDITION_CHOICES)

    class Meta:
        ordering = ('-date',)

    def save(self, *args, **kwargs):
        self.location = get_city_location(self.city)
        super(Book, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('books:book_detail', args =[str(self.id)])

    def __str__(self) -> str:
                return self.name

class BookImage(models.Model):
    book = models.ForeignKey(Book, default=None, on_delete = models.CASCADE)
    image = models.ImageField(
            upload_to=user_directory_path,
            null=True,
            blank=True)
    thumbnail = models.ImageField(
            upload_to=user_directory_path2,
            null=True)

