from django.db import models
from django.contrib.auth import get_user_model
from books.models import Book
from django.utils.text import slugify
# Create your models here.

class SavedBooks(models.Model):
    save_by_user = models.ForeignKey(get_user_model(), on_delete = models.CASCADE)
    books_saved = models.ForeignKey(Book, on_delete = models.CASCADE)
    create_at = models.DateTimeField(auto_now_add = True)

    slug = models.SlugField(unique=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.save_by_user)
        super(get_user_model(), self).save(*args, **kwargs)

    def __str__(self):
        return self.books_saved
