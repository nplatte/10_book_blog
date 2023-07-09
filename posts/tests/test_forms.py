from posts.forms import PostModelForm
from django.test import TestCase

class TestPostModelForm(TestCase):

    def test_form_successful_submit(self):
        new_form = PostModelForm({'title': 'A', 'book_author': 'V.E. Schwab',
                                  'book_title': 'A Darker Side of Magic',
                                  'post': 'blahblahblah'})
        self.assertTrue(new_form.is_valid())
        