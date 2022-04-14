import imp
import uuid
from django.shortcuts import render, redirect
from django.http import HttpResponse
from utils import user_handle, post_handle
import requests

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
        # filename = request.FILES['filename']
        # for filename, file in request.FILES.iteritems():
        #     name = request.FILES[filename].name
        #     print(name)
        post = files.get('usr_post')
        headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'image/png'
                }

        # print(type(post))

        url = "https://qofpjxi1zg.execute-api.ap-south-1.amazonaws.com/v6/ccl-practical-1019153/test1"
        r = requests.put(url=url,data=post,headers=headers)

        print(r)
        print(r.content)


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
        print(description)
        # print(response.json())
        # post_handle.insert_one(
        #     {
        #         '_id':str(uuid.uuid4()),
        #         'userid':userid,
        #         ''
        #         }
        #         )
    return render(request,'newPost.html')
