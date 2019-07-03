import os
from django.db import transaction
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from rest_framework.response import Response
from rest_framework.views import  APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string

from users.models import Profile, Follower
from media.models import Post, Comment, fs as PhotoStorage

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

@api_view(['POST',])
@permission_classes([IsAuthenticated, ])
@transaction.atomic
def MakePost(request):
    """
    View function for making posts.

    Returns Post upon success.
    """
    #[Needs Validator]

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

    return Response({ 'post_success' : True})

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

        return Response({ 'comment_success': True })
