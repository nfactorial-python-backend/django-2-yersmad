from django.shortcuts import render, get_object_or_404, get_list_or_404, reverse, redirect
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group


from .models import News, Comment
from .forms import NewsForm, SignUpForm


# Create your views here.
def sign_up(request):
   if request.method == 'POST':
       form = SignUpForm(request.POST)
       if form.is_valid():
           user = form.save()

           group = Group.objects.get(name='Default')
           group.user_set.add(user)
           
           login(request, user)
           return redirect("/news")
   else:
       form = SignUpForm()

   return render(request, 'registration/sign_up.html', {"form": form})


def index(request):
    news = News.objects.order_by("-created_at").all()
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


@login_required(login_url="/login")
def post_comment(request, news_id):
    if request.method == "POST":
        db_news = News.objects.get(pk=news_id)
        comment = request.POST["comment"]
        new_comment = Comment(content=comment, news_id=news_id)
        new_comment.author = request.user
        db_news.has_comments = True
        new_comment.save()
        db_news.save()
        
        return redirect(reverse("news:detail", args=(db_news.id,)))

    return render(request, "news/post_comment.html", {"news_id": news_id})


@login_required(login_url="/login")
def post_news(request):
    if request.method == "POST":
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()

            return redirect(reverse("news:detail", args=(news.id,)))

    return render(request, "news/post_news.html")


# class UpdateNewsView(View):
#     def get(self, request, news_id):
#         news = get_object_or_404(News, pk=news_id)
#         form = NewsForm()
#         return render(request, "news/update_news.html", {"form": form, "news": news})

#     def post(self, request, news_id):
#         news = get_object_or_404(News, pk=news_id)
#         form = NewsForm(request.POST, instance=news)
#         if form.is_valid():
#             title = form.cleaned_data["title"]
#             content = form.cleaned_data["content"]
#             news.title = title
#             news.content = content
#             news.save()

#             return redirect(reverse("news:detail", args=(news.id,)))

@login_required(login_url="/login")
@permission_required("news.edit_news", login_url="/login/")
def update_news(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    if request.method == "POST":
        if request.user == news.author or request.user.has_perm("news.change_news"):
            form = NewsForm(request.POST, instance=news)
            if form.is_valid():
                title = form.cleaned_data["title"]
                content = form.cleaned_data["content"]
                news.title = title
                news.content = content
                news.save()

                return redirect(reverse("news:detail", args=(news.id,)))

    return render(request, "news/update_news.html", {"form": form, "news": news})


@login_required(login_url="/login")
@permission_required("news.delete_news", login_url="/login/")
def delete_news(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    if request.method == "POST":
        if request.user == news.author or request.user.has_perm("news.delete_news"):
            news.delete()

        return redirect(reverse("news:index"))


@login_required(login_url="/login")
@permission_required("comment.delete_comment", login_url="/login/")
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == "POST":
        if request.user == comment.author or request.user.has_perm("comment.delete_comment"):
            comment.delete()

        return redirect(reverse("news:news"))
