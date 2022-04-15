import uuid
from django.shortcuts import render, redirect
from django.http import HttpResponse
from utils import user_handle, post_handle
import requests
import json

file = open('config.json')
config_json = json.load(file)
file.close()

# Create your views here.
def index(request):
    return render(request, 'index.html')

def profile(request, userid, profileid):
    user = user_handle.find_one({'_id':userid})    
    profile = user_handle.find_one({'_id':profileid})
    print(profile)
    posts = list(post_handle.find({'userID':profileid}))
    print(posts)
    context = {
        'posts' : posts,
        'profile' : profile,
        'user' : user,
        'noOfPosts' : len(posts),
        'followers' : len(profile['followers']),
        'following' : len(profile['following']),
        'imageLink' : config_json['S3-image']
    }
    return render(request,'profile.html',context)

def feed(request):
    return render(request,'feed.html')

def explore(request, userid):
    user = user_handle.find_one({'_id':userid})
    people = list(user_handle.find({}))
    context = {
        'user':user,
        'people':people,
        'imageLink' : config_json['S3-image']
    }
    return render(request,'explore.html',context)

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
            return redirect(profile,userid=user['_id'],profileid=user['_id'])
        
    return render(request, 'index.html')


def newPost(request,userid):
    if request.method == 'POST':
        files = request.FILES  # multivalued dict
        print(type(files))
        print(files)
        
        post = files.get("image")
        location = request.POST['location']
        description = request.POST['description']
        url = "https://qofpjxi1zg.execute-api.ap-south-1.amazonaws.com/v6"+"/ccl-practical-1019153/"+str(userid)
        headers={
            "Content-Type":"image/jpeg",
            "User-Agent":"PostmanRuntime/7.28.4",
            "Accept":"*/*",
            "Accept":"application/json"
        }
        response = requests.put(url=url,headers=headers ,data=post)
        print(type(post))
        print(location)
        # print(response.json())
        # post_handle.insert_one(
        #     {
        #         '_id':str(uuid.uuid4()),
        #         'userid':userid,
        #         ''
        #         }
        #         )
    return render(request,'newPost.html')
