from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required

from users.models import Profile, Follower

# APIview for following and unfollowing a user
class FollowView(APIView):
    """
    View function for following another user.
    """
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        # note that this is sometimes interpretted as a str
        # this is not good and if I have time I would like to
        # write some request validator
        # same applies for any API Call from here on with comment
        # [Needs Validator]
        pk = request.data.get('pk')
        if pk:
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
                user = Profile.objects.get(pk)
                follower_obj = request.user.get_follower_object(pk)
                unfollowed = follower_obj.user_followed
                follower_obj.delete()
                
                return HttpResponseRedirect(reverse('media:profile', kwargs= {'username': user.username}))
        else:
            raise ValueError('Pk required')
