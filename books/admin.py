from django.contrib import admin
from .models import Book, Category
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display=['name','slug']
    prepopulated_fields={'slug':('name',)}

class BookAdmin(admin.ModelAdmin):
    list_display=['name','category','price','date','seller']
    list_filter =['category','date']
    list_editable = ['price']
admin.site.register(Category,CategoryAdmin)
admin.site.register(Book,BookAdmin)
