from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required

from users.models import Profile, Follower

@login_required
def index(request):
    return HttpResponse("Test. Here we go.")

# APIview for following and unfollowing a user
@login_required
class FollowView(APIView):
    """
    View function for following another user.

    Returns the follower object upon success

    Arguments:
    request - A WSGI Request object
    pk - A number representing the primary key of the user being followed
    """
    def get(self, request):
        return HttpResponse("Test. Here we go.")
    def post(self,request):
        if not request.user:
            raise ValueError('Not logged in')

        if request.user.is_following_user(pk):
            raise ValueError('You are already following this user')
        else:
            followed = Follower.objects.create(
                    user_followed_id=pk,
                    user_following=request.user.pk
            )
            return Response({'followed' : True})

    def delete(self, request):
        if not request.user:
            raise ValueError('Not logged in')

        if not request.user.is_following_user(pk):
            raise ValueError('You must be following to unfollow.')
        else:
            follower_obj = request.user.get_follower_object(pk)
            unfollowed = follower_obj.user_followed
            follower_obj.delete()
            return Response({'unfollowed': True})
