from posts.forms import PostModelForm, TagForm
from django.test import TestCase
from posts.models import Tag

class TestPostModelForm(TestCase):

    def setUp(self) -> None:
        form_data = {
            'title': 'A', 
            'book_author': 'V.E. Schwab',
            'book_title': 'A Darker Side of Magic',
            'post': 'blahblahblah'}
        self.test_form = PostModelForm(form_data)
        return super().setUp()

    def test_form_successful_submit(self):
        self.assertEqual(self.test_form.errors, {})
        self.assertTrue(self.test_form.is_valid())

    def test_form_has_right_identifying_information(self):
        form_as_html = self.test_form.as_p()
        self.assertIn('id="author_entry"', form_as_html)
        self.assertIn('id="title_entry"', form_as_html)
        self.assertIn('id="post_entry"', form_as_html)
        self.assertIn('id="book_title_entry"', form_as_html)


class TestTagModelForm(TestCase):

    def setUp(self):
        self.good_form_data = {'author_tag_list': '#Steven_King',
                               'general_tag_list': '#start',
                               'book_tag_list': '#TheDarkTower'}
        self.bad_form_data = {'author_tag_list': '#Steven_King',
                               'general_tag_list': '#start',
                               'book_tag_list': 'TheDarkTower'}
        self.test_form = TagForm(self.good_form_data)

    def test_successful_form_submit(self):
        self.assertEqual(self.test_form.errors, {})
        self.assertTrue(self.test_form.is_valid())

    def test_form_has_right_identifying_info(self):
        html = self.test_form.as_p()
        self.assertIn('id="general_tag_entry"', html)
        self.assertIn('id="author_tag_entry"', html)
        self.assertIn('id="book_tag_entry"', html)

    def test_custom_validation_catches_missing_hashtag(self):
        tag_form = TagForm(self.bad_form_data)
        self.assertEqual(tag_form.errors['book_tag_list'], ['# missing in tag'])
        self.assertFalse(tag_form.is_valid())
