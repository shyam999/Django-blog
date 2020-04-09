from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from core.models import Category, Post
from users.models import UserProfile
from django.contrib.auth.models import User
import pytest

@pytest.mark.django_db
class CategoryTest(TestCase):

    def create_category(self, title="test"):
        return Category.objects.create(title=title)

    def test_category_creation(self):
        c = self.create_category()
        self.assertTrue(isinstance(c, Category))
        self.assertEqual(c.__str__(), c.title)

@pytest.mark.django_db
class PostTest(TestCase):
    
    def setUp(self):
        self.category = Category.objects.create(title='testcat', slug='testcat',)
        self.user = User.objects.create_user(username="name", email="email@mail.com", password="Pass12345")
        self.userprofile = UserProfile.objects.create(user=self.user, bio="great guy")

    def create_post(self, title="product"):
        return Post.objects.create(id=12, category=self.category, title=title, author=self.userprofile, created_date=timezone.now())

    def test_post_creation(self):
        p = self.create_post()
        self.assertTrue(isinstance(p, Post))
        self.assertEqual(p.__str__(), p.title)

@pytest.mark.django_db
class UserProfileTest(TestCase):

        def setUp(self):
            self.user = User.objects.create_user(username="name", email="email@mail.com", password="Pass12345")

        def create_userprofile(self):
            return UserProfile.objects.create(user=self.user, bio="great guy")

        def test_userprofile_create(self):
            u = self.create_userprofile()
            self.assertTrue(isinstance(u, UserProfile))
