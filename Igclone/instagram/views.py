from django.shortcuts import render, redirect
from django.http import HttpResponse
from utils import user_handle

# Create your views here.
def index(request):
    return render(request, 'index.html')

def profile(request, userid):
    users = user_handle.find({})
    print(list(users))
    return render(request,'profile.html')

def feed(request):
    return render(request,'feed.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = user_handle.find_one(
            {
                'username':username,
                'password':password
            }
             )

        if user is not None:
            return redirect(profile,userid=user['_id'])
        
    return render(request, 'index.html')


def newPost(request):
    return render(request,'newPost.html')
