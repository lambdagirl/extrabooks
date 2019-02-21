from django.db import models
from books.models import Book
from django.contrib.auth import get_user_model
# Create your models here.

class Message(models.Model):
    author = models.ForeignKey(
            get_user_model(),
            related_name = 'author_messages',
            on_delete = models.CASCADE,)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def last_10_messages(self):
        return Message.objects.order_by('timestamp').all()[:10]
