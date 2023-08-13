from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:news_id>/", views.detail, name="detail"),
    path("<int:news_id>/post_comment", views.post_comment, name="post_comment"),
    path("post_news/", views.post_news, name="post_news"),
]   
