from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect

from .models import News, Comment


# Create your views here.
def index(request):
    news = get_list_or_404(News.objects.order_by("-created_at"))
    context = {"news": news}
    return render(request, "news/index.html", context)

def detail(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    try:
        comments = Comment.objects.get(news_id=news_id)
    except Comment.DoesNotExist:
        comments = None

    if not comments:
        context = {"news": news}
        return render(request, "news/detail.html", context)
    else:
        comments = get_list_or_404(Comment, news_id=news_id)
        context = {"news": news, "comments": comments}
        return render(request, "news/detail.html", context)

def post_comment(request, news_id):
    comments = request.POST["comments"]

    if comments != "":
        news = get_object_or_404(News, pk=news_id)
        db_comments = Comment(content=comments, news=news)
        db_comments.save()

        return HttpResponseRedirect(reverse("news:post_comment", args=news_id,))
    
    return HttpResponseRedirect(reverse("news:post_comment", args=news_id,))

def post_news(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        news = News(title=title, content=content)
        news.save()

        return HttpResponseRedirect(reverse("news:post_news", args=news.id))

    return render(request, "news/post_news.html")
