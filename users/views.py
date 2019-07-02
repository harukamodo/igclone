from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required

from users.models import Profile, Follower

@login_required
def index(request):
    return HttpResponse("Test. Here we go.")

# APIview for following and unfollowing a user
class FollowView(APIView):
    """
    View function for following another user.

    Returns the follower object upon success

    Arguments:
    request - A WSGI Request object
    pk - A number representing the primary key of the user being followed
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if not request.user:
            return HttpResponse('u suck')

        return HttpResponse(request.user)

    def post(self,request):
        # note that this is sometimes interpretted as a __str__
        # this is not good and if I have time I would like to
        # write some request validator
        # same applies for any API Call from here on with comment
        # [Needs Validator]
        pk = request.data.get('pk')
        if request.data.get('pk'):
            if request.user.is_following_user(pk):
                raise ValueError('You are already following this user')
            elif not Profile.objects.filter(pk=pk).exists():
                raise ValueError('User does not exist')
            else:

                print('hello')
                followed = Follower.objects.create(
                    user_followed_id=pk,
                    user_follower_id=request.user.pk
                )
                return Response({'followed' : True})
        else:
            raise ValueError('Pk required')

    def delete(self, request):
        # [Needs Validator]
        pk = request.data.get('pk')
        if request.data.get('pk'):
            if not request.user.is_following_user(pk):
                raise ValueError('You must be following to unfollow.')
            elif not Profile.objects.filter(pk=pk).exists():
                raise ValueError('User does not exist')
            else:
                follower_obj = request.user.get_follower_object(pk)
                unfollowed = follower_obj.user_followed
                follower_obj.delete()
                return Response({'unfollowed': True})
        else:
            raise ValueError('Pk required')
