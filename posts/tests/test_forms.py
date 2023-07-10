from posts.forms import PostModelForm, TagForm
from django.test import TestCase
from posts.models import Tag

class TestPostModelForm(TestCase):

    def test_form_successful_submit(self):
        new_form = PostModelForm({'title': 'A', 'book_author': 'V.E. Schwab',
                                  'book_title': 'A Darker Side of Magic',
                                  'post': 'blahblahblah'})
        self.assertEqual(new_form.errors, {})
        self.assertTrue(new_form.is_valid())

    def test_form_has_right_identifying_information(self):
        form = PostModelForm()
        form_as_html = form.as_p()
        self.assertIn('id="author_entry"', form_as_html)
        self.assertIn('id="title_entry"', form_as_html)
        self.assertIn('id="post_entry"', form_as_html)
        self.assertIn('id="book_title_entry"', form_as_html)


class TestTagModelForm(TestCase):

    def test_successful_form_submit(self):
        self.assertEqual(len(Tag.objects.all()), 0)
        tag_form = TagForm({'tag_list': '#Steven King'})
        self.assertEqual(tag_form.errors, {})
        self.assertTrue(tag_form.is_valid())
        self.assertEqual(len(Tag.objects.all()), 1)

    def test_form_has_right_identifying_info(self):
        form = TagForm()
        html = form.as_p()
        self.assertIn('id="tag_entry"', html)

    def test_form_can_create_multiple_tags(self):
        self.assertEqual(len(Tag.objects.all()), 0)
        tag_form = TagForm({'tag_list': '#Steven King #Dark Tower'})
        self.assertTrue(tag_form.is_valid())
        self.assertEqual(len(Tag.objects.all()), 2)
