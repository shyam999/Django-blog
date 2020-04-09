from django.test import TestCase, Client
from django.urls import reverse
from core.models import Category, Post
from users.models import UserProfile
from django.contrib.auth.models import User
import pytest

@pytest.mark.django_db
class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="name", email="email@mail.com",
        password="Pass12345")
        self.userprofile = UserProfile.objects.create(user=self.user, bio="great guy")
        self.category = Category.objects.create(title='fashion', slug='fashion',)
        self.post = Post.objects.create(category=self.category, pk=15, title='postfashion',
        image ='static/blog/img/sam.png', author=self.userprofile)

    def test_blog_view(self):
        response = self.client.get(reverse('core:blog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/display/post_list.html')

    def test_post_detail_view(self):
        response = self.client.get(reverse('core:post_detail', kwargs={'pk': 15}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/display/post_detail.html')

    def test_post_detail_view_error(self):
        response = self.client.get(reverse('core:post_detail', kwargs={'pk': 16}))
        self.assertEqual(response.status_code, 404)

    def test_post_share_view(self):
        response = self.client.get(reverse('core:post_share', kwargs={'pk': 15}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/display/post_share.html')