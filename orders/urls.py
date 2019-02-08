from django.urls import path, include
from django.conf.urls import url
from .views import make_offer,create_order

app_name = "extrabooks_app"

urlpatterns = [
    path('make_offer/<seller>',make_offer,name='make_offer'),
    path('create_order/',create_order,name='create_order')
]
