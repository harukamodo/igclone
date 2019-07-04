from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth import logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required

from users.models import Profile, Follower

def SearchProfiles(request):
    search = request.GET.get('search','')
    user_set = Profile.objects.filter(username__icontains=search).exclude(username=request.user.username)
    
    context = {
        'searched': list(user_set)
    }
    template = loader.get_template('users/search_results.html')
    return HttpResponse(template.render(context, request))
# APIview for following and unfollowing a user
@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def FollowView(request, pk):
    if request.user.is_following_user(pk):
        raise ValueError('You are already following this user')
    elif not Profile.objects.filter(pk=pk).exists():
        raise ValueError('User does not exist')
    else:
        user = Profile.objects.get(pk=pk)
        followed = Follower.objects.create(
            user_followed=user,
            user_follower_id=request.user.pk
        )
        
        return HttpResponseRedirect(reverse('media:profile', kwargs={ 'username': user.username }))

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def UnfollowView(request, pk):
    if not request.user.is_following_user(pk):
        raise ValueError('You must be following to unfollow.')
    elif not Profile.objects.filter(pk=pk).exists():
        raise ValueError('User does not exist')
    else:
        user = Profile.objects.get(pk=pk)
        follower_obj = request.user.get_follower_object(pk)
        unfollowed = follower_obj.user_followed
        follower_obj.delete()
        print(reverse('media:profile',kwargs={'username':user.username}))        
        return HttpResponseRedirect(reverse('media:profile', kwargs= {'username': user.username}))

def LogoutView(request):
    logout(request)
    return redirect('/admin/login/')
