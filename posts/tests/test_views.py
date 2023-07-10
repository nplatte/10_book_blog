from django.test import TestCase
from django.urls import reverse

from posts.models import Post, Tag
from posts.forms import PostModelForm, TagForm
from django.contrib.auth.models import User
from posts.views import create_post_page

# test that the context is being passed correctly
# test that the forms are the right forms  to use
# 
class TestHomeView(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('home_page'))

    def test_view_returns_right_template(self):
        self.assertTemplateUsed('posts/home.html')

    def test_context_contains_post_requests(self):
        Post.objects.create(title='test')
        response = self.client.get(reverse('home_page'))
        self.assertEqual(len(response.context['posts']), 1)

    def test_view_tag_context(self):
        t1 = Tag.objects.create(tag_name='general', group_name='general')
        t2 = Tag.objects.create(tag_name='book', group_name='author')
        t3 = Tag.objects.create(tag_name='author', group_name='book')
        self.assertEqual(len(Tag.objects.all()), 3)
        general_tags = self.response.context['general_tags']
        self.assertEqual(len(general_tags), 1)
        self.assertEqual(general_tags[0].id, t1.id)
        author_tags = self.response.context['author_tags']
        self.assertEqual(len(author_tags), 1)
        self.assertEqual(author_tags[0].id, t2.id)
        book_series_tags = self.response.context['book_tags']
        self.assertEqual(len(book_series_tags), 1)
        self.assertEqual(book_series_tags[0].id, t3.id)


class TestGETCreatePostView(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(username='test_user', password='passweod')
        self.client.force_login(self.test_user)
        self.response = self.client.get(reverse('create_post'))

    def test_view_returns_right_template(self):
        self.assertTemplateUsed('posts/create.html')

    def test_view_form_context(self):
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
            'post': 'blahblahblabla',
            'tag_list': '#start #V.E._Schwab'
        }
        self.response = self.client.post(reverse('create_post'), context)
        return super().setUp()
    
    def test_post_request_redirects_to_post_page(self):
        self.assertRedirects(self.response, reverse('home_page'))    

    def test_view_makes_new_post_on_POST_request(self):
        self.assertEqual(1, len(Post.objects.all()))

    def test_POST_request_with_tags_creates_new_blog_post_with_tags(self):
        new_post = Post.objects.all()[0]
        same_post = Post.objects.filter(tags__tag_name='start')
        self.assertEqual(1, len(same_post))
        self.assertEqual(new_post.id, same_post[0].id)