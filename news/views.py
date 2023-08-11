from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect

from .models import News, Comment


# Create your views here.
def index(request):
    news = get_list_or_404(News.objects.order_by("-created_at"))
    context = {"news": news}
    return render(request, "news/index.html", context)

def detail(request, new_id):
    news = get_object_or_404(News, pk=new_id)
    comments = get_list_or_404(Comment, news_id=new_id)
    context = {"news": news, "comments": comments}
    return render(request, "news/news_by_id.html", context)

def create_news(request):
    title = request.POST.get("title")
    content = request.POST.get("content")
    return HttpResponseRedirect("news/index.html",)
