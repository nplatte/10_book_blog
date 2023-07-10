from posts.forms import PostModelForm, TagForm
from django.test import TestCase
from posts.models import Tag

class TestPostModelForm(TestCase):

    def test_form_successful_submit(self):
        t1, t2 = Tag(tag_name='t1'), Tag(tag_name='t2')
        t1.save()
        t2.save()
        new_form = PostModelForm({'title': 'A', 'book_author': 'V.E. Schwab',
                                  'book_title': 'A Darker Side of Magic',
                                  'post': 'blahblahblah', 'tags': [t1, t2]})
        self.assertEqual(new_form.errors, {})
        self.assertTrue(new_form.is_valid())

    def test_form_has_right_identifying_information(self):
        form = PostModelForm()
        form_as_html = form.as_p()
        self.assertIn('id="author_entry"', form_as_html)
        self.assertIn('id="title_entry"', form_as_html)
        self.assertIn('id="post_entry"', form_as_html)
        self.assertIn('id="book_title_entry"', form_as_html)
        self.assertIn('id="tag_entry"', form_as_html)

    def test_form_validation_checks_for_hashtag(self):
        new_form = PostModelForm({'title': 'A', 'book_author': 'V.E. Schwab',
                                  'book_title': 'A Darker Side of Magic',
                                  'post': 'blahblahblah', 'tags': 'test'})
        self.assertEqual(len(new_form.errors['tags']), 1)
        self.assertEqual(new_form.errors['tags'][0], 'Add a hashtag infront of the tag')


class TestTagModelForm(TestCase):

    def test_successful_form_submit(self):
        pass

    def test_form_has_right_identifying_info(self):
        pass

    def test_form_can_create_multiple_tags(self):
        pass

