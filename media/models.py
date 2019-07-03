from django.db import models

class Post(models.Model):
    posted_by = models.ForeignKey(
        'users.Profile',
        related_name="posts",
        on_delete=models.CASCADE
    )
    caption = models.CharField(max_length=500, null=True, blank=True)
    post_date = models.DateTimeField(auto_now_add=True, db_index=True)

class Comment(models.Model):
    posted_on = models.ForeignKey(
        'media.Post',
        related_name="comments",
        on_delete=models.CASCADE
    )
    posted_by = models.ForeignKey(
        'users.Profile',
        related_name="commented",
        on_delete=models.CASCADE
    )
    comment = models.CharField(max_length=500)
    post_date = models.DateTimeField(auto_now_add=True, db_index=True)
