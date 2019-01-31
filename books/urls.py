from django.urls import path, include
from django.conf.urls import url

from .views import (
    BookListView,
    BookUpdateView,
    BookDeleteView,
    BookDetailView,
    BookCreateView,
    MyBookListView,
    search,
    BookListbyCategoryView,
    book_list_by_tag,
    )

app_name = "extrabooks_app"

urlpatterns = [
    path('', BookListView.as_view(), name ='book_list'),
    path('tag/<slug:tag_slug>/',book_list_by_tag, name='book_list_by_tag' ),
    path('<int:pk>/edit/', BookUpdateView.as_view(), name = 'book_edit'),
    path('<int:pk>/delete/', BookDeleteView.as_view(), name = 'book_delete'),
    path('<int:pk>/', BookDetailView.as_view(), name = 'book_detail'),
    path('new/', BookCreateView.as_view(), name = 'book_new'),
    path('my_book_list/', MyBookListView.as_view(), name = 'my_book_list'),
    path('search/', search, name = 'search'),
    path('explore/<int:pk>/', BookListbyCategoryView.as_view(), name='explore'),
]
