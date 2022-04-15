from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login',views.login,name="login"),
    path('profile/<slug:userid>/<slug:profileid>', views.profile, name='profile'),
    path('follow/<slug:userid>/<slug:profileid>', views.follow, name='follow'),
    path('feed', views.feed, name='feed'),
    path('explore/<slug:userid>', views.explore, name='explore'),
    path('newPost/<slug:userid>', views.newPost, name='newPost'),
]