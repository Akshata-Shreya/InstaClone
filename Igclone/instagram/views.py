
import uuid
from django.shortcuts import render, redirect
from django.http import HttpResponse
from utils import user_handle, post_handle
import requests
from datetime import datetime
import json
from operator import itemgetter

# file = open('config.json')
# config_json = json.load(file)
# file.close()

# Create your views here.
def index(request):
    return render(request, 'login.html')

def profile(request, userid, profileid):

    user = user_handle.find_one({'_id':userid})    
    profile = user_handle.find_one({'_id':profileid})
    posts = list(post_handle.find({'userID':profileid}))

    file = open('config.json')
    config_json = json.load(file)
    file.close()

    for post in posts :
        post['numberOfLikes'] = len(post['likedby'])
            # posts.append(post)

    context = {
        'userid':userid,
        'img_url': profilePicUrlfromUserID(userid),
        'posts' : posts,
        'profile' : profile,
        'user' : user,
        'noOfPosts' : len(posts),
        'followers' : len(profile['followers']),
        'following' : len(profile['following']),
        'imageLink' : config_json['S3-image']
    }
    return render(request,'profile.html',context)

def viewImage(request,userid,postid):
    file = open('config.json')
    config_json = json.load(file)
    file.close()

    post = post_handle.find_one({'_id':postid})
    
    dp_url = profilePicUrlfromUserID(userid)

    user = user_handle.find_one({'_id':post['userID']})

    parameters = {
        'userid':userid,
        'postid':postid,
        'post':post,
        'posted_by':user['name'],
        'numberOfLikes' : len(post['likedby']),
        'date':post['timestamp'].date(),
        'time':post['timestamp'].time(),
        'img_url':dp_url,
        'imageLink' : config_json['S3-image']
    }
    return render (request,'image-detail.html',parameters)

def feed(request,userid):
    user = user_handle.find_one({'_id':userid})
    posts = []
    for followee in user['following']:
        followeeUser = user_handle.find_one({'_id':followee})
        # print(follower)
        followerPosts = list(post_handle.find({'userID':followee}))
        for post in followerPosts:
            post['user'] = followeeUser
            post['numberOfLikes'] = len(post['likedby'])
            post['date'] = post['timestamp'].date()
            post['time'] = post['timestamp'].time()
            posts.append(post)
    # print(posts)
    sorted_list = sorted(posts,key=itemgetter('timestamp'), reverse=True )
    print(sorted_list)
    file = open('config.json')
    config_json = json.load(file)
    file.close()
    parameters = {
        'user':user,
        'userid':userid,
        'img_url': profilePicUrlfromUserID(userid),
        'posts':sorted_list,
        'imageLink' : config_json['S3-image']
    }
    # sorted_list = sorted(patientRecords,key=itemgetter('uploadedOn'), reverse=True )
    return render(request,'feed.html',parameters)

def follow(request, userid, profileid):
    # user = user_handle.find_one({'_id':userid}) 
    
    user_handle.update_one(
            {'_id':userid},
            [
                {'$set':{'following':{'$concatArrays':['$following',[profileid]]}}}
            ]
        )  
    user_handle.update_one(
            {'_id':profileid},
            [
                {'$set':{'followers':{'$concatArrays':['$followers',[userid]]}}}
            ]
        )     
    return redirect(profile,userid=userid,profileid=profileid)

def explore(request, userid):
    user = user_handle.find_one({'_id':userid})
    people = list(user_handle.find({}))

    file = open('config.json')
    config_json = json.load(file)
    file.close()

    context = {
        'userid':userid,
        'img_url':profilePicUrlfromUserID(userid),
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
        
        # utc_datetime = datetime.now().astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")

        post_object = {
            '_id' : postid,
            'postID':postid,
            'userID':userid,
            'location':location,
            'description':description,
            'timestamp':datetime.now(),
            'likedby':[]
        }        

        post_handle.insert_one(post_object)

        return redirect(profile,userid=userid,profileid=userid)

    if request.method == 'GET': 

        user = user_handle.find_one({'_id':userid})  
        name = user['name'] 

        url = profilePicUrlfromUserID(userid)

        parameters = {
            'userid':userid,
            'name':name,
            'img_url': url
        }
        
        return render(request,'newPost.html',parameters)



def likePost(request,postid,userid,returnPage):
    post = post_handle.find_one({'_id':postid})
    likedby = post['likedby']
    if userid not in likedby:
        post_handle.update_one(
            {'_id':postid},
            [
                {'$set':{'likedby':{'$concatArrays':['$likedby',[userid]]}}}
            ]
        )
    if returnPage=="fromFeed":
        return redirect (feed,userid=userid)
    # else:
    #     post_handle.update_one(
    #         {'_id':postid},
    #         [
    #             {'$pull':{'likedby':userid}}
    #         ]
    #     )
    return redirect (viewImage,userid=userid,postid=postid)


def profilePicUrlfromUserID(userid):
    file = open('config.json')
    config_json = json.load(file)
    file.close()

    base_url = config_json['S3-image']

    url = base_url+'usr-'+str(userid)

    return url

