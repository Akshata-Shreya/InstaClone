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

    file = open('config.json')
    config_json = json.load(file)
    file.close()

    if request.method == 'POST':
        files = request.FILES

        post = files.get('usr_post')
        # location = request.POST['location']
        # description = request.POST['description']
        location = request.POST.get('location','')
        description = request.POST.get('description','')

        headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'image/png',
                    "Accept":"*/*",
                }

        base_url = config_json['S3-upload']
        folder = config_json['folder']

        postid = str(uuid.uuid4())

        url = base_url+folder+postid

        response = requests.put(url=url, headers=headers, data=post)
        
        post_object = {
            '_id' : postid,
            'postID':postid,
            'userID':userid,
            'location':location,
            'description':description
        }        

        post_handle.insert_one(post_object)

    # if request.method == 'GET': 

    user = user_handle.find_one({'_id':userid})  
    name = user['name'] 

    base_url = config_json['S3-image']

    url = base_url+'usr-'+userid

    parameters = {
        'userid':userid,
        'name':name,
        'img_url': url
    }
    
    return render(request,'newPost.html',parameters)
