from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login',views.login,name="login"),
    path('profile/<slug:userid>', views.profile, name='profile'),
    path('feed/<slug:userid>', views.feed, name='feed'),
    path('profile/<slug:userid>/<slug:profileid>', views.profile, name='profile'),
    path('follow/<slug:userid>/<slug:profileid>', views.follow, name='follow'),
    path('explore/<slug:userid>', views.explore, name='explore'),
    path('newPost/<slug:userid>', views.newPost, name='newPost'),
    path('viewImage/<slug:userid>/<slug:postid>',views.viewImage,name='viewImage'),
    path('likePost/<slug:postid>/<slug:userid>/<slug:returnPage>',views.likePost,name="likePost"),
    path('signup',views.signup, name="signup")
]