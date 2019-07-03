from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import  APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required

from users.models import Profile, Follower
from media.models import Post, Comment

@api_view(['POST',])
@permission_classes([IsAuthenticated, ])
def MakePost(request):
    """
    View function for making posts.

    Returns Post upon success.
    """
    #[Needs Validator]

    caption = request.data.get('caption')
    post = Post.objects.create(posted_by=request.user, caption=caption)
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
