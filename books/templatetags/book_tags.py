from django import template
from ..models import Book, Category

register = template.Library()

@register.simple_tag
def total_books():
    return Book.objects.count()

@register.inclusion_tag('books/all_categories.html')
def show_all_categories():
    all_categories = Category.objects.all()
    return {'all_categories':all_categories}
