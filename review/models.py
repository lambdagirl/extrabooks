from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from books.models import Book
from django.shortcuts import get_object_or_404
from django.db.models import Avg

class PublishedManager(models.Manager):

    use_for_related_fields = True

    def published(self, **kwargs):
        return self.filter(pub_date__lte=timezone.now(), **kwargs)

    def create_review(cls, reviewer,rating,descriptions):
        review = cls(reviewer=reviewer)
        # do something with the book
        return review

    def book_score(self, book_id):
        book = None
        book= get_object_or_404(Book,id=book_id)
        reviews = BookReview.objects.filter(book__in=[book])
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        return avg_rating

class BookReview(models.Model): # The Category table name that inherits models.Model
    book = models.ForeignKey(
            Book,
            on_delete = models.CASCADE,)
    rating = models.IntegerField(null=True, blank=True)
    descriptions = models.CharField(max_length=255)
    pub_date = models.DateTimeField()
    reviewer = models.ForeignKey(
            get_user_model(),
            on_delete = models.CASCADE,)
    # add our custom model manager
    objects = PublishedManager()
