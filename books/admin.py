from django.contrib import admin
from .models import Book, Category
from django.contrib.gis.admin import OSMGeoAdmin

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display=['name','slug']
    prepopulated_fields={'slug':('name',)}

class BookAdmin(OSMGeoAdmin):
    list_display=['name','category','price','date','seller','city','location', 'condition']
    list_filter =['category','date']
    list_editable = ['price','city']
admin.site.register(Category,CategoryAdmin)
admin.site.register(Book,BookAdmin)
