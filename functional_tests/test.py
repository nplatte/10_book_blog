from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class TestCanPost(StaticLiveServerTestCase):

    def test_user_can_make_post(self):
        pass