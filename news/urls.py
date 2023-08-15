from django.urls import path
from . import views


app_name = "news"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:news_id>/", views.detail, name="detail"),
    path("<int:news_id>/create_comment", views.post_comment, name="post_comment"),
    path("create_news/", views.post_news, name="post_news"),
    path("<int:news_id>/edit", views.UpdateNewsView.as_view(), name="edit_news"),

]
