from django.urls import path

from .views import SignUpView,ProfieView,EditProfileView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name ='signup'),
    path('<int:pk>/', ProfieView.as_view(), name ='profile'),
    path('settings/<int:pk>', EditProfileView.as_view(), name= 'settings')
]
