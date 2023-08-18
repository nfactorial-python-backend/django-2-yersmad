from django.urls import path
from . import views


app_name = "news"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:news_id>/", views.detail, name="detail"),
    path("<int:news_id>/create_comment", views.post_comment, name="post_comment"),
    path("create_news/", views.post_news, name="post_news"),
    path("<int:news_id>/edit", views.update_news, name="edit_news"),
    path("<int:news_id>/delete", views.delete_news, name="delete_news"),
    path("<int:comment_id>/delete", views.delete_comment, name="delete_comment"),

    # path("api/add", views.api_add, name="api_add"),
    path("api/news", views.NewsAddListView.as_view(), name="api_list"),
    path("api/news/<int:pk>/", views.NewsDetailView.as_view(), name="api_news_detail"),
]
