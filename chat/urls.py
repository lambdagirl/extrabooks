
from django.urls import path
from .views import index, room

app_name = "extrabooks_app"

urlpatterns = [
    path('', index, name = 'index'),
    path('<room_name>/', room, name = 'room'),

]
