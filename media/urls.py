from django.urls import path
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^post/$', views.MakePost, name="follow"),
    url(r'^comment/(?P<pk>\w+)/$', views.MakeComment, name="comment"),
]
