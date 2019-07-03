from django.urls import path
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from . import views
from media.models import fs

urlpatterns = [
    url(r'^profile/(?P<username>\w+)/$', views.ProfilePage, name="profile"),
    url(r'^post/', include([
        url(r'^(?P<pk>\w+)/$', views.PostPage, name="post"),
        url(r'^$', views.MakePost, name="make_post"),
        ])),
    url(r'^comment/(?P<pk>\w+)/$', views.MakeComment, name="comment"),
]
