
from django.contrib import admin
from .models import BookReview

# Register your models here.

class BookReviewAdmin(admin.ModelAdmin):
    list_display=['book','rating','pub_date','reviewer']

admin.site.register(BookReview,BookReviewAdmin)
