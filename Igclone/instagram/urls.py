from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login',views.login,name="login"),
    path('profile/<slug:userid>', views.profile, name='profile'),
    path('feed/<slug:userid>', views.feed, name='feed'),
    path('newPost/<slug:userid>', views.newPost, name='newPost'),
    path('viewImage/<slug:postid>',views.viewImage,name='viewImage')
]