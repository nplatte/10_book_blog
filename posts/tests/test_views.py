from django.test import TestCase
from django.urls import reverse

from posts.views import create_post_page

class TestCreatePostView(TestCase):

    def test_view_returns_right_template(self):
        self.client.get(reverse('create_post'))
        self.assertTemplateUsed('posts/create.html')

    def test_post_request_redirects_to_post_page(self):
        context = {
            'author_name': 'V.E. Schwab',
            'book_name': 'A Darker Shade of Magic',
            'post': 'blahblahblabla'
        }
        response = self.client.post(reverse('create_post'), context)
        self.assertRedirects(response, reverse('view_post'))

        