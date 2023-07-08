from posts.models import Post, Tag
from django.test import TestCase



class TestPost(TestCase):

    def test_string_representation(self):
        test_title = 'New Post!'
        post = Post.objects.create(title=test_title)
        self.assertEqual(str(post), test_title)

    def test_can_filter_posts_by_tags(self):
        t1, t2, t3 = 'Title1', 'Title2', 'Title3'
        p1 = Post.objects.create(title=t1)
        p2 = Post.objects.create(title=t2)
        p3 = Post.objects.create(title=t3)
        tag1 = Tag.objects.create(tag_name='tag1')
        tag2 = Tag.objects.create(tag_name='tag2')
        tag3 = Tag.objects.create(tag_name='tag3')

        p1.tags.add(tag1)
        p2.tags.add(tag1)
        p3.tags.add(tag1)
        p2.tags.add(tag2)
        p3.tags.add(tag2)
        p3.tags.add(tag3)
        
        posts = Post.objects.filter(tags__tag_name='tag1')
        self.assertEqual(len(posts), 3)
        posts = Post.objects.filter(tags__tag_name='tag2')
        self.assertEqual(len(posts), 2)
        posts = Post.objects.filter(tags__tag_name='tag3')
        self.assertEqual(len(posts), 1)


class TestTag(TestCase):

    def test_string_representation(self):
        test_tag_name = "V.W. Schwab"
        tag = Tag.objects.create(tag_name=test_tag_name)
        self.assertEqual(str(tag), test_tag_name)
