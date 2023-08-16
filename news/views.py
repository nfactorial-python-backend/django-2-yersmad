from django.shortcuts import render, get_object_or_404, get_list_or_404, reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import View


from .models import News, Comment
from .forms import NewsForm


# Create your views here.
def index(request):
    news = get_list_or_404(News.objects.order_by("-created_at"))
    context = {"news": news}
    return render(request, "news/news.html", context)

def detail(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    try:
        comments = list(Comment.objects.filter(news_id=news_id).all())
    except Comment.DoesNotExist:
        comments = None

    if not comments:
        context = {"news": news}
        return render(request, "news/detail.html", context)
    else:
        comments = list(Comment.objects.filter(news_id=news_id).order_by("-created_at").all())
        context = {"news": news, "comments": comments}
        return render(request, "news/detail.html", context)

def post_comment(request, news_id):
    if request.method == "POST":
        db_news = News.objects.get(pk=news_id)
        comment = request.POST["comment"]
        new_comment = Comment(content=comment, news_id=news_id)
        db_news.has_comments = True
        new_comment.save()
        db_news.save()
        
        return HttpResponseRedirect(reverse("news:detail", args=(db_news.id,)))

    return render(request, "news/post_comment.html", {"news_id": news_id})

def post_news(request):
    if request.method == "POST":
        form = NewsForm(request.POST)
        if form.is_valid():
            news = News(title=form.cleaned_data["title"], content=form.cleaned_data["content"])
            news.save()

            return HttpResponseRedirect(reverse("news:detail", args=(news.id,)))

    return render(request, "news/post_news.html")

class UpdateNewsView(View):
    def get(self, request, news_id):
        news = get_object_or_404(News, pk=news_id)
        form = UpdateNewsForm()
        return render(request, "news/update_news.html", {"form": form, "news": news})

    def post(self, request, news_id):
        news = get_object_or_404(News, pk=news_id)
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            news = News(title=form.cleaned_data["title"], content=form.cleaned_data["content"])
            news.save()

            return HttpResponseRedirect(reverse("news:detail", args=(news.id,)))
