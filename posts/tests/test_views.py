from django.test import TestCase
from django.urls import reverse

from posts.models import Post
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
        response = self.client.get(reverse('home_page'))
        Post.objects.create(title='test')
        self.assertEqual(len(response.context['posts']), 1)


class TestCreatePostView(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(username='test_user', password='passweod')

    def test_view_returns_right_template(self):
        self.client.force_login(self.test_user)
        self.client.get(reverse('create_post'))
        self.assertTemplateUsed('posts/create.html')

    def test_view_requires_login(self):
        response = self.client.get(reverse('create_post'))
        self.assertRedirects(response, '/login/?next=/posts/create-post')

    def test_post_request_redirects_to_post_page(self):
        self.client.force_login(self.test_user)
        context = {
            'author_name': 'V.E. Schwab',
            'book_name': 'A Darker Shade of Magic',
            'post': 'blahblahblabla'
        }
        response = self.client.post(reverse('create_post'), context)
        self.assertRedirects(response, reverse('view_post'))

        