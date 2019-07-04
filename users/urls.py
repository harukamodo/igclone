from django.urls import path
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^logout/$', views.LogoutView, name="logout"),    
    url(r'^search/$', views.SearchProfiles, name="search"),
    url(r'^follow/(?P<pk>\w+)/$', views.FollowView, name="follow"),
    url(r'^unfollow/(?P<pk>\w+)/$', views.UnfollowView, name="unfollow")
]
