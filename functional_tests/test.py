from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By
from posts.models import Post, Tag

from time import sleep

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
    
    def _log_in_from_home(self):
        sign_in_button = self.browser.find_element(By.ID, 'nav_sign_in')
        sign_in_button.click()
        username_box = self.browser.find_element(By.ID, 'username_entry')
        password_box = self.browser.find_element(By.ID, 'password_entry')
        username_box.send_keys(self.test_username)
        password_box.send_keys(self.test_password)
        self.browser.find_element(By.ID, 'login_button').click()
    
    def test_I_can_log_in(self):
        # I see the nav bar with a Home, Find Post, About, and Sign In and click sign in
        sign_in_button = self.browser.find_element(By.ID, 'nav_sign_in')
        sign_in_button.click()
        title = self.browser.title
        self.assertEqual('Log In', title)
        # this takes me to a log in screen where I enter in my credentials
        username_box = self.browser.find_element(By.ID, 'username_entry')
        password_box = self.browser.find_element(By.ID, 'password_entry')
        username_box.send_keys(self.test_username)
        password_box.send_keys(self.test_password)
        self.browser.find_element(By.ID, 'login_button').click()
        self.assertEqual(self.browser.title, 'Create Post')
        # I enter them in and am taken to a new screen
        self.assertEqual(self.browser.title, 'Create Post')

    def test_user_can_make_post(self):
        # I navigate to the website
        # I see no posts up so I decide to make one
        post_number = self.browser.find_elements(By.CLASS_NAME, 'post')
        self.assertEqual(0, len(post_number))
        # I log in to create a post
        self._log_in_from_home()
        # decide my first book will be V.E. Shwwab's "A Darker Shade of Magic"
        book_title = "A Darker Shade of Magic"
        book_author = "V. E. Shwab"
        # I enter in the author and book name
        author_entry_box = self.browser.find_element(By.ID, 'author_entry')
        title_entry_box = self.browser.find_element(By.ID, 'title_entry')
        author_entry_box.send_keys(book_author)
        title_entry_box.send_keys('First Post!')
        boot_title_entry_box = self.browser.find_element(By.ID, 'book_title_entry')
        boot_title_entry_box.send_keys(book_title)
        # I add the tags that are appropriate
        tags = '#book1'
        tag_entry = self.browser.find_element(By.ID, 'general_tag_entry')
        tag_entry.send_keys(tags)
        tags = '#ShadeofMagic'
        tag_entry = self.browser.find_element(By.ID, 'book_tag_entry')
        tag_entry.send_keys(tags)
        tags = '#V.E.Shwab'
        tag_entry = self.browser.find_element(By.ID, 'author_tag_entry')
        tag_entry.send_keys(tags)
        # I add my thoughts on the first two chapters and hit post
        thoughts = 'blahblahblahblah'
        thoughts_entry = self.browser.find_element(By.ID, 'post_entry')
        thoughts_entry.send_keys(thoughts)
        post_button = self.browser.find_element(By.ID, 'create_post_button')
        post_button.click()
        # I click the home button and see my post on the recent posts
        post_number = self.browser.find_elements(By.CLASS_NAME, 'post')
        self.assertEqual(1, len(post_number))

    def test_i_can_filter_posts_by_tags(self):
        p1, p2, p3 = Post.objects.create(title='Post 1'), Post.objects.create(title='Post 2'), Post.objects.create(title='Post 3')
        t1, t2, t3 = Tag.objects.create(tag_name='start', group_name='general'), Tag.objects.create(tag_name='middle', group_name='author'), Tag.objects.create(tag_name='end', group_name='book')
        p1.tags.add(t1)
        p2.tags.add(t2)
        p3.tags.add(t3)
        self.browser.refresh()
        # I open the website and see three posts with the most recent at the top
        post_count = len(self.browser.find_elements(By.CLASS_NAME, 'post'))
        self.assertEqual(3, post_count)
        tag_count = len(self.browser.find_elements(By.CLASS_NAME, 'tag'))
        self.assertEqual(3, tag_count)
        # I decide I want to only see what post was the start of the series
        # I click the permanent tags on the side to filter the posts and only see one now
        start_tag = self.browser.find_elements(By.ID, 'tag_start')
        start_tag.click()
        post_count = len(self.browser.find_elements(By.CLASS_NAME, 'post'))
        self.assertEqual(1, post_count)
        # I click it again and all of the posts appear
        start_tag.click()
        post_count = len(self.browser.find_elements(By.CLASS_NAME, 'post'))
        self.assertEqual(3, post_count)
        