from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    has_comments = models.BooleanField(default=False)

    def __str__(self):
        return self.title, self.content

class Comment(models.Model):
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
