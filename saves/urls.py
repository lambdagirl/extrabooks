from django.urls import path

from .views import SavedBooksView

urlpatterns = [
    path('saves/<slug>', SavedBooksView.as_view(), name = 'saves')
    ]
