from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request): 
    return HttpResponse("Test. Here we go.")

# view for following and unfollowing a user
def Follow(request):
    return HttpResponse("Follow me!!")

