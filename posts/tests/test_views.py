from django.test import TestCase
from django.urls import reverse

from posts.views import create_post_page

class TestCreatePostView(TestCase):

    def test_view_returns_right_template(self):
        self.client.get(reverse('create_post'))
        self.assertTemplateUsed('posts/create.html')