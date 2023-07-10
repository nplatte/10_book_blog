from django.test import TestCase
from django.urls import reverse

from posts.models import Post
from posts.forms import PostModelForm, TagForm
from django.contrib.auth.models import User
from posts.views import create_post_page

# test that the context is being passed correctly
# test that the forms are the right forms  to use
# 
class TestHomeView(TestCase):

    def test_view_returns_right_template(self):
        self.client.get(reverse('home_page'))
        self.assertTemplateUsed('posts/home.html')

    def test_context_contains_post_requests(self):
        Post.objects.create(title='test')
        response = self.client.get(reverse('home_page'))
        
        self.assertEqual(len(response.context['posts']), 1)


class TestGETCreatePostView(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(username='test_user', password='passweod')
        self.client.force_login(self.test_user)
        self.response = self.client.get(reverse('create_post'))

    def test_view_returns_right_template(self):
        self.assertTemplateUsed('posts/create.html')

    def test_view_context(self):
        form = self.response.context['new_post_form']
        self.assertIsInstance(form, PostModelForm)
        form = self.response.context['post_tags_form']
        self.assertIsInstance(form, TagForm)


class TestPOSTCreatePostView(TestCase):
    
    def setUp(self) -> None:
        self.test_user = User.objects.create_user(username='test_user', password='passweod')
        self.client.force_login(self.test_user)
        context = {
            'title': 'Test Post',
            'book_author': 'V.E. Schwab',
            'book_title': 'A Darker Shade of Magic',
            'post': 'blahblahblabla'
        }
        self.response = self.client.post(reverse('create_post'), context)
        return super().setUp()
    
    def test_post_request_redirects_to_post_page(self):
        self.assertRedirects(self.response, reverse('home_page'))    

    def test_view_makes_new_post_on_POST_request(self):
        self.assertEqual(1, len(Post.objects.all()))


        