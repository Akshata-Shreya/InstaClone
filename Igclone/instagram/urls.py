from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('feed', views.feed, name='feed'),
    path('newPost', views.newPost, name='newPost'),
]