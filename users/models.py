from django.db import models
from django.contrib.auth.models import (
        AbstractBaseUser, BaseUserManager)
from django.db.models.signals import post_save

class ProfileManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, password, bio=None):
        if not email:
            raise ValueError('Email is Required')
        if not username:
            raise ValueError('Username is Required')
        if not (first_name and last_name):
            raise ValueError('First Name and Last Name are Required')
        if not password:
            raise ValueError('Password is required')

        profile = self.model(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=self.normalize_email(email),
                bio=bio)
        profile.set_password(password)
        profile.save()
        return profile

    def create_superuser(self, username, first_name, last_name, email, password):
        profile = self.create_user(
            username,
            first_name,
            last_name,
            email,
            password
        )
        profile.is_admin = True
        profile.save(using=self._db)
        return profile

class Profile(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=150)
    bio = models.TextField(max_length=500, null=True, blank=True)
    add_date = models.DateTimeField(auto_now_add=True, db_index=True)
    is_admin = models.BooleanField(default=False)

    objects = ProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True
    @property
    def is_staff(self):
        return self.is_admin

    # returns followers in a list
    def get_followers(self):
        followers = [ f.user_follower for f in self.followers.all() ]
        return followers

    # returns users profile is following in a list
    def get_following(self):
        following = [ f.user_followed for f in self.following.all() ]
        return following

    # returns a bool depending on if another user is following this user
    def is_followed_by_user(self, pk):
        followed_by = int(pk) in [ f.pk for f in self.get_followers()]
        return followed_by

    # returns a bool depending on if this user is following another user
    def is_following_user(self, pk):
        following =  int(pk) in [ f.pk for f in  self.get_following()]
        return following

    # returns the following object where this user is user_followed
    def get_follower_object(self, pk):
        following = None
        if self.is_following_user(pk):
            following = Follower.objects.get(
                    user_follower=self,
                    user_followed_id=pk)
        return following

    def get_followed_by_object(self, pk):
        followed_by = None
        if self.is_followed_by_user(pk):
            followed_by = Follower.objects.get(
                    user_follower_id=pk,
                    user_followed=self)
        return followed_by



class Follower(models.Model):
    #user being followed
    user_followed = models.ForeignKey(
        Profile,
        related_name="followers",
        on_delete=models.CASCADE
    )
    #this user is the follower
    user_follower = models.ForeignKey(
        Profile,
        related_name="following",
        on_delete=models.CASCADE
    )
    add_date = models.DateTimeField(auto_now_add=True, db_index=True)
