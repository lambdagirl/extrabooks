from django.contrib import admin
from .models import Book, Category, Images
from django.contrib.gis.admin import OSMGeoAdmin

# Register your models here.
class ImagesInline(admin.StackedInline):
    model = Images

class CategoryAdmin(admin.ModelAdmin):
    list_display=['name','slug']
    prepopulated_fields={'slug':('name',)}

class BookAdmin(OSMGeoAdmin):
    list_display=['name','category','price','date','seller','city','location', 'condition', 'isbn']
    list_filter =['category','date']
    list_editable = ['price','city']
    inlines = [ImagesInline]

admin.site.register(Category,CategoryAdmin)
admin.site.register(Book,BookAdmin)
