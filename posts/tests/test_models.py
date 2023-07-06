from posts.models import Post
from django.test import TestCase



class TestPost(TestCase):

    def test_string_representation(self):
        test_title = 'New Post!'
        post = Post.objects.create(title=test_title)
        self.assertEqual(post, test_title)

