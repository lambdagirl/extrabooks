from django.contrib import admin
from .models import Order, OfferBook
# Register your models here.

class OfferBookInline(admin.TabularInline):
    model = OfferBook
    raw_id_fields=['book']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name', 'email','address','postal_code',
                    'city','paid','created','updated']

admin.site.register(Order,OrderAdmin)
admin.site.register(OfferBook)
