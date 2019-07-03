import os
from functools import reduce
from django.db import transaction
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import  APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string

from users.models import Profile, Follower
from media.models import Post, Comment, fs as PhotoStorage

@login_required
def UserFeed(request):
    """
    view to return user feed
    """
    template = loader.get_template('media/feed.html')
    user = request.user
    following = user.get_following()
    #combining the posts of all users that are followed by this profile
    posts = reduce(lambda x,y: x+y,[ list(f.posts.all()) for f in following ], [])
    #sorting in order of most recent
    posts = sorted(posts, key=lambda p: p.post_date, reverse=True)
    context = {
        'post_set': posts
    }
    return HttpResponse(template.render(context, request))

@login_required
def ProfilePage(request, username):
    """
    Profile page that displays all the user's photos
    """
    profile = Profile.objects.get(username=username)
    template = loader.get_template('media/profile.html')
    posts = profile.get_posts()
    context = {
        'profile': profile,
        'post_set': posts
    }
    return HttpResponse(template.render(context, request))

@login_required
def PostPage(request, pk):
    """
    Post page that displays all the comments
    """
    post = Post.objects.get(pk=pk)
    template = loader.get_template('media/post.html')
    comments = post.comments.order_by('-post_date').all()
    context = {
        'post': post,
        'comment_set': comments
    }
    return HttpResponse(template.render(context, request))


class MakePost(APIView):
    """
    View function for making posts.

    Returns Post upon success.
    """
    #[Needs Validator]
    permissions_classes = (IsAuthenticated,)
    
    def get(self, request):
        user = request.user
        template = loader.get_template('media/make_post.html')
        
        return HttpResponse(template.render({}, request))

    @transaction.atomic
    def post(self, request):
        caption = request.data.get('caption')
        photo = request.FILES['photo']
        print(photo.name)
        post = Post.objects.create(
            posted_by=request.user,
            photo=photo,
            caption=caption
        )

        name = "%d_%d_" % (request.user.pk, post.pk)
        name = name + get_random_string(length=32) + "." + post.photo.name.split('.')[-1]
        old_path = post.photo.path
        post.photo.name = name
        path = PhotoStorage.path(name)
        os.rename(old_path, path)
        post.save()

        return HttpResponseRedirect(reverse('media:post', kwargs={ 'pk': post.pk}))

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def MakeComment(request, pk):
    """
    """
    #[Needs Validator]

    comment = request.data.get('comment')
    if not comment:
        raise ValueError('Caption is required')
    else:
        comment = Comment.objects.create(
            posted_by=request.user,
            posted_on_id=pk,
            comment=comment
        )

        return HttpResponseRedirect(reverse('media:post', kwargs={'pk': comment.posted_on.pk}))
