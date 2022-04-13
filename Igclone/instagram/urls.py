from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login',views.login,name="login"),
    path('profile/<int:userid>', views.profile, name='profile'),
    path('feed', views.feed, name='feed'),
    path('newPost/<int:userid>', views.newPost, name='newPost'),
]