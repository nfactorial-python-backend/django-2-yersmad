from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class News(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    has_comments = models.BooleanField(default=False)


class Comment(models.Model):
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE)

