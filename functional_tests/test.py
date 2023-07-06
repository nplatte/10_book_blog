from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By

class TestCanPost(StaticLiveServerTestCase):

    def setUp(self):
        # creates user and goes to the home page
        self.test_username = 'nplatte'
        self.test_password = 'swordpass123567'
        User.objects.create_user(self.test_username, 'test@test.com', self.test_password)
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def test_user_can_make_post(self):
        # I navigate to the website
        # I see no posts up so I decide to make one
        post_number = self.browser.find_elements(By.CLASS_NAME, 'post')
        self.assertEqual(0, len(post_number))
        # I see the nav bar with a Home, Find Post, About, and Sign In and click sign in
        home_button = self.browser.find_element(By.ID, 'nav_home')
        find_post_button = self.browser.find_element(By.ID, 'nav_find_posts')
        about_button = self.browser.find_element(By.ID, 'nav_about')
        sign_in_button = self.browser.find_element(By.ID, 'nav_sign_in')
        sign_in_button.click()
        # this takes me to a log in screen where I enter in my credentials
        title = self.browser.title
        self.assertEqual('Log In', title)
        username_box = self.browser.find_element(By.ID, 'username_entry')
        password_box = self.browser.find_element(By.ID, 'password_entry')
        # I enter them in and am taken to a new screen
        # decide my first book will be V.E. Shwwab's "A Darker Shade of Magic"
        # I enter in the author and book name
        # I add the tags that are appropriate
        # I add my thoughts on the first two chapters and hit post
        # I click the home button and see my post on the recent posts
        post_number = self.browser.find_elements(By.CLASS_NAME, 'post')
        self.assertEqual(1, len(post_number))
        # I click the new post and see what just got done posting
        