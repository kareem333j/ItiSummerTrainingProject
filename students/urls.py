from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('main', Main.as_view(), name='main'),
    path('profile/<int:pk>', profile, name='profile'),
    path('profile/<int:pk>/edit', EditProfile.as_view(), name='profile.edit'),
    path('users/all', users, name='users'),
    path('users/search/<str:item>', search_users, name='users.search'),
]