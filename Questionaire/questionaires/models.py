from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    heading = models.CharField(max_length=10000, null=True, blank=True)
    post = models.TextField()

    def __str__(self):
        return self.heading


class Reply(models.Model):
    sno = models.AutoField(primary_key=True)
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    replay = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.email
