from django.urls import path

from .views import SignUpView,ProfieView,EditProfileView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name ='signup'),
    path('u/<slug>/', ProfieView.as_view(), name ='profile'),
    path('<slug>/editing', EditProfileView.as_view(), name= 'settings')

]
