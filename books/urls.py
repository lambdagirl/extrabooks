from django.urls import path, include

from .views import (
    BookListView,
    BookUpdateView,
    BookDeleteView,
    BookDetailView,
    BookCreateView,
    MyBookListView,
    search
    )

app_name = "extrabooks_app"

urlpatterns = [
    path('', BookListView.as_view(), name ='book_list'),
    path('<int:pk>/edit/', BookUpdateView.as_view(), name = 'book_edit'),
    path('<int:pk>/delete/', BookDeleteView.as_view(), name = 'book_delete'),
    path('<int:pk>/', BookDetailView.as_view(), name = 'book_detail'),
    path('new/', BookCreateView.as_view(), name = 'book_new'),
    path('my_book_list/', MyBookListView.as_view(), name = 'my_book_list'),
    path('search/', search, name = 'search'),


]
