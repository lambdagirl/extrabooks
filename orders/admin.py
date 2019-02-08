from django.contrib import admin
from .models import Order,Offer,OfferItem
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name', 'email','address','postal_code',
                    'city','paid','created','updated']
    list_filter = ['paid','created','updated']
    #inlines = [OrderItemInline]

class OfferItemInline(admin.TabularInline):
    model = OfferItem
    raw_id_fields=['book']


class OfferAdmin(admin.ModelAdmin):
    list_display =['user', 'offer_price']
    inlines = [OfferItemInline]

admin.site.register(Order,OrderAdmin)
#admin.site.register(OrderItem)
admin.site.register(Offer,OfferAdmin)
admin.site.register(OfferItem)
