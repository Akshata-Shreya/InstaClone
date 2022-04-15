
import uuid
from django.shortcuts import render, redirect
# from django.http import HttpResponse
from utils import user_handle, post_handle
import requests
import json

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


def newPost(request,userid):
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

        

        file = open('config.json')
        config_json = json.load(file)
        file.close()

        base_url = config_json['S3-upload']
        folder = config_json['folder']

        postid = str(uuid.uuid4())

        url = base_url+folder+postid

        response = requests.put(url=url, headers=headers, data=post)
        
        print(response.text)

        post_object = {
            '_id' : postid,
            'postID':postid,
            'userID':userid,
            'location':location,
            'description':description
        }

        post_handle.insert_one(post_object)

    if request.method == 'POST': 

        user = user_handle.find_one({'userID':userid})  
         
        
        return render(request,'newPost.html',{'userid':userid})
