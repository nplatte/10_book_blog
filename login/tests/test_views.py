from django.test import  LiveServerTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime

class TestLoginPage(LiveServerTestCase):

    '''the login page needs to be the first page people see
    it needs to use the right template
    redirect good users to month view
    redirect bad users to login page'''

    def setUp(self):
        self.test_username = 'winkstiddly'
        self.test_password = 'password123'
        User.objects.create_user(username=self.test_username, email='test@test.com', password=self.test_password)

    def tearDown(self):
        pass

    def test_login_uses_right_template(self):
        response = self.client.get(reverse('login_page'))
        self.assertTemplateUsed(response,'login/login.html')

    def test_login_redirects_to_create_post_on_success(self):
        response = self.client.post(reverse('login_page'), {'username': self.test_username, 'password': self.test_password}, follow=True)
        self.assertRedirects(response, f'/posts/create-post')

    def test_login_redirects_to_login_on_fail(self):
        response = self.client.post(reverse('login_page'), {'username': self.test_username, 'password': 'wrong_password'}, follow=True)
        self.assertRedirects(response, reverse('login_page'))

    def test_view_requires_login(self):
        response = self.client.get(reverse('create_post'))
        self.assertRedirects(response, '/login/?next=/posts/create-post')
