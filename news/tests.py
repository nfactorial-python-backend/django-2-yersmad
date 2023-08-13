from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import News, Comment
# Create your tests here.

class NewsModelTest(TestCase):
    def test_has_comments_true(self):
        temp_news = News(title="Test", content="test content",  has_comments=False)
        temp_news.save()
        temp_comment = Comment(content="test comment", news_id=temp_news.id)
        temp_comment.save()

        if temp_comment.news_id == temp_news.id:
            temp_news.has_comments = True
        self.assertIs(True, temp_news.has_comments)

    def test_has_comments_false(self):
        temp_news = News(title="Test", content="test content")
        temp_news.save()
        self.assertIs(False, temp_news.has_comments)

class NewsViewsTest(TestCase):
    def test_index_page(self):
        temp_news1 = News(title="Test", content="test content",  has_comments=False)
        temp_news2 = News(title="Test2", content="test content2",  has_comments=False)
        temp_news1.save()
        temp_news2.save()

        response = self.client.get(reverse("news:index"))

        self.assertIs(200, response.status_code)
        self.assertQuerysetEqual([temp_news2, temp_news1], response.context["news"])

    def test_detail_page(self):
        temp_news = News(title="Test", content="test content",  has_comments=False)
        temp_news.save()

        response = self.client.get(reverse("news:detail", args=(temp_news.id,)))

        self.assertIs(200, response.status_code)
        self.assertEqual(temp_news, response.context["news"])

    def test_detail_page_comments(self):
        temp_news = News(title="Test", content="test content",  has_comments=False)
        temp_news.save()
        temp_comment1 = Comment(content="test comment", news_id=temp_news.id)
        temp_comment2 = Comment(content="test comment2", news_id=temp_news.id)
        temp_comment1.save()
        temp_comment2.save()

        response = self.client.get(reverse("news:detail", args=(temp_news.id,)))

        self.assertIs(200, response.status_code)
        self.assertQuerysetEqual([temp_comment2, temp_comment1], response.context["comments"])
