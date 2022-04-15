from inspect import Parameter
import uuid
from django.shortcuts import render, redirect
from django.http import HttpResponse
from utils import user_handle, post_handle
import requests
import json

# file = open('config.json')
# config_json = json.load(file)
# file.close()

# Create your views here.
def index(request):
    return render(request, 'login.html')

def profile(request, userid):
    user = user_handle.find_one({'_id':userid})
    print(user)
    posts = list(post_handle.find({'userID':userid}))
    print(posts)
    file = open('config.json')
    config_json = json.load(file)
    file.close()
    context = {
        'userid':userid,
        'img_url': profilePicUrlfromUserID(userid),
        'posts' : posts,
        'user' : user,
        'noOfPosts' : len(posts),
        'imageLink' : config_json['S3-image']
    }
    return render(request,'profile.html',context)

def feed(request,userid):
    parameters = {
        'userid':userid,
        'img_url': profilePicUrlfromUserID(userid)
    }
    return render(request,'feed.html',parameters)

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
            return redirect(feed,userid=user['_id'])
        
    return render(request, 'login.html')


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

    url = profilePicUrlfromUserID(userid)

    parameters = {
        'userid':userid,
        'name':name,
        'img_url': url
    }
    
    return render(request,'newPost.html',parameters)

def viewImage(request,postid):
    file = open('config.json')
    config_json = json.load(file)
    file.close()

    post = post_handle.find_one({'_id':postid})
    dp_url = profilePicUrlfromUserID(post['userID'])
    parameters = {
        'postid':postid,
        'img_url':dp_url,
        'base_url':config_json['S3-image']
    }
    return render (request,'image-detail.html',parameters)


def profilePicUrlfromUserID(userid):
    file = open('config.json')
    config_json = json.load(file)
    file.close()

    base_url = config_json['S3-image']

    url = base_url+'usr-'+userid

    return url

