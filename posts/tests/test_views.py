from django.test import TestCase
from django.urls import reverse

from posts.models import Post, Tag
from posts.forms import PostModelForm, TagForm
from django.contrib.auth.models import User
from posts.views import _add_tags

# test that the context is being passed correctly
# test that the forms are the right forms  to use
# 
class TestHomeView(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('home_page'))

    def test_view_returns_right_template(self):
        self.assertTemplateUsed('posts/home.html')

    def test_context_contains_posts(self):
        Post.objects.create(title='test')
        response = self.client.get(reverse('home_page'))
        self.assertEqual(len(response.context['posts']), 1)

    def test_context_contains_tags(self):
        t1 = Tag.objects.create(tag_name='general', group_name='general')
        t2 = Tag.objects.create(tag_name='book', group_name='author')
        t3 = Tag.objects.create(tag_name='author', group_name='book')

        self.response = self.client.get(reverse('home_page'))
        tag_group_list = self.response.context['tag_groups']

        self.assertEqual(len(tag_group_list), 3)
        general_tags = tag_group_list[0]
        self.assertEqual(general_tags[0], Tag.objects.filter(group_name='general')[0])
        author_tags = tag_group_list[1]
        self.assertEqual(author_tags[0], Tag.objects.filter(group_name='author')[0])
        book_tags = tag_group_list[2]
        self.assertEqual(book_tags[0], Tag.objects.filter(group_name='book')[0])


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
            'general_tag_list': '#start',
            'author_tag_list': '#V.E._Schwab',
            'book_tag_list': '#A_Darker_Shade_of_Magic'
        }
        self.response = self.client.post(reverse('create_post'), context)
        return super().setUp()
    
    def test_post_request_redirects_to_post_page(self):
        self.assertRedirects(self.response, reverse('home_page'))    

    def test_view_makes_new_post_on_POST_request(self):
        self.assertEqual(1, len(Post.objects.all()))

    def test_POST_request_with_tags_creates_new_blog_post_with_tags(self):
        new_post = Post.objects.all()[0]
        same_post = Post.objects.filter(tags__tag_name='#start')
        self.assertEqual(1, len(same_post))
        self.assertEqual(new_post.id, same_post[0].id)


class TestAJAXViewPOST(TestCase):

    def test_base_case(self):
        request = self.client.post(reverse('ajax_post'), {})
        self.assertEqual(request.status_code, 200)


class TestHelperFunc(TestCase):

    def setUp(self) -> None:
        self.new_post = Post.objects.create(title='Test Post')
        self.tags = '#start #author_name'
        return super().setUp()

    def test_add_tags_base_case(self):
        self.assertEqual(len(Post.objects.filter(tags__tag_name='#start')), 0)
        _add_tags(self.new_post, self.tags, 'general')
        self.assertEqual(len(Post.objects.filter(tags__tag_name='#start')), 1)

    def test_add_tags_two_tags(self):
        self.assertEqual(len(Post.objects.filter(tags__tag_name='#start')), 0)
        _add_tags(self.new_post, self.tags, 'general')
        self.assertEqual(len(Post.objects.filter(tags__tag_name='#author_name')), 1)
        self.assertEqual(len(Post.objects.filter(tags__tag_name='#start')), 1)

    def test_new_tags_are_not_created_if_they_already_exist(self):
        t1 = Tag.objects.create(tag_name='#start')
        t2 = Tag.objects.create(tag_name='#author_name')
        self.assertEqual(len(Tag.objects.all()), 2)
        _add_tags(self.new_post, self.tags, 'general')
        self.assertEqual(len(Tag.objects.all()), 2)