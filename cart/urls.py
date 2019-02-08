from django.urls import path, include
from django.conf.urls import url
from .views import cart_detail,cart_add,cart_remove

app_name = "extrabooks_app"

urlpatterns = [
    path('', cart_detail, name = 'cart_detail'),
    path('add/<int:book_pk>/', cart_add, name = 'cart_add'),
    path('remove/<int:book_pk>/',cart_remove, name ='cart_remove', ),
]
