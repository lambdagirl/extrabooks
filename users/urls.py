from django.urls import path

from .views import SignUpView,ProfieView,EditProfileView,user_follow,dashboard

urlpatterns = [
    path('signup/', SignUpView.as_view(), name ='signup'),
    path('follow/', user_follow, name ="user_follow"),
    path('u/<slug>/', ProfieView.as_view(), name ='profile'),
    path('<slug>/editing', EditProfileView.as_view(), name= 'settings'),
    path('dashboard/',dashboard, name="dashboard"),
]
