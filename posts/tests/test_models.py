from posts.models import Post, Tag
from django.test import TestCase



class TestPost(TestCase):

    def test_string_representation(self):
        test_title = 'New Post!'
        post = Post.objects.create(title=test_title)
        self.assertEqual(str(post), test_title)


class TestTag(TestCase):

    def test_string_representation(self):
        test_tag_name = "V.W. Schwab"
        tag = Tag.objects.create(tag_name=test_tag_name)
        self.assertEqual(str(tag), test_tag_name)
