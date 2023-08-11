from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    path("", views.index, name="start_page"),
    path("<int:new_id>/", views.detail, name="news_by_id"),
    path("create_news/", views.create_news, name="create_news"),
    
]   
