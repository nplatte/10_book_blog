from posts.forms import PostModelForm
from django.test import TestCase

class TestPostModelForm(TestCase):

    def test_form_successful_submit(self):
        new_form = PostModelForm({'title': 'A', 'book_author': 'V.E. Schwab',
                                  'book_title': 'A Darker Side of Magic',
                                  'post': 'blahblahblah'})
        self.assertTrue(new_form.is_valid())

    def test_form_has_right_identifying_information(self):
        form = PostModelForm()
        form_as_html = form.as_p()
        self.assertIn('id="author_entry"', form_as_html)
        self.assertIn('id="title_entry"', form_as_html)
        self.assertIn('id="post_entry"', form_as_html)
        self.assertIn('id="book_title_entry"', form_as_html)

        