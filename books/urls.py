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
    get_distance,
    BookListbyCategoryView,
    book_list_by_tag,
    book_list_category,
    #BookCreateByISBNView,
    book_create_by_ISBN,
    book_create_by_ISBN_2,
    book_ranking,
    sort
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
    path('search/get_distance', get_distance, name = 'get_distance'),
    path('sort/', sort, name = 'sort'),
    path('categories/<slug:category_slug>/', book_list_category, name='book_list_category'),
    path('book_new_by_ISBN/', book_create_by_ISBN, name= 'book_new_by_ISBN'),
    path('book_by_isbn/', book_create_by_ISBN_2, name='book_by_isbn'),
    path('ranking/', book_ranking, name="ranking")
]
