from json import dumps
from django.test import TestCase, Client

from .models import Post, User 


# Create your tests here.
class TestApp(TestCase):
    def setUp(self):
        self.client = Client()
    

    def test_register_user(self):
        """Registers a user"""
        response = self.client.post("/register", {
            "username": "mario_test", 
            "password": "m",
            "confirmation": "m",
            "email": "privateaccmariomolinito729@gmail.com"})
        user = User.objects.get(username="mario_test")
        self.assertTrue(user)


    def test_login_user(self):
        """Creates user, attempts to log in user after."""
        self.test_register_user()
        logged_in = self.client.login(username="mario_test", password="m")
        self.assertTrue(logged_in)


    def test_creating_post(self):
        """Creates one post, checks the database for one post"""
        # log user in
        self.test_login_user()
        response = self.client.post("/posts", {"title": "Testing Post", 
            "text": "This is the text"})
        self.assertEqual(response.status_code, 200)


    def test_editing_post(self):
        # login, create the post
        self.test_creating_post()
        response = self.client.patch(f"/posts?id=1", 
                dumps({"title": "Updated post"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.get(id=1).title, "Updated post")

    
    def test_getting_post_by_id(self):
        self.test_creating_post()
        response = self.client.get("/posts?id=1")
        self.assertEqual(response.json().get("title"), "Testing Post")


    def test_get_all_post(self):
        self.test_creating_post()
        response = self.client.get("/posts")
        self.assertEqual(type(response.json().get("posts")), type([]))
        self.assertTrue(len(response.json().get("posts")) >= 1)
