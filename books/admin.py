from django.contrib import admin
from .models import Book, Category, BookImage
from django.contrib.gis.admin import OSMGeoAdmin
from django.utils.html import format_html
# Register your models here.
class BookImageInline(admin.StackedInline):
    model = BookImage
    list_display = ('thumbnail_tag')
    readonly_fields = ('thumbnail',)
    def thumbnail_tag(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="%s"/>' % obj.thumbnail.url
            )
        return "-"
    thumbnail_tag.short_description = "Thumbnail"

class CategoryAdmin(admin.ModelAdmin):
    list_display=['name','slug']
    prepopulated_fields={'slug':('name',)}

class BookAdmin(OSMGeoAdmin):
    list_display=['name','category','price','date','seller','city','location', 'condition', 'isbn','rating']
    list_filter =['category','date']
    list_editable = ['price','city']
    inlines = [BookImageInline]

admin.site.register(Category,CategoryAdmin)
admin.site.register(Book,BookAdmin)
