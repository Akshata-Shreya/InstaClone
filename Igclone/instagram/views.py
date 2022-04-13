from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def profile(request):
    return render(request,'profile.html')

def feed(request):
    return render(request,'feed.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        print("username ", username)
        print("password ", password)
        return render(request, 'index.html')
