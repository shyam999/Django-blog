from django.test import SimpleTestCase
from django.urls import reverse, resolve
from core.views import *
import pytest

@pytest.mark.django_db
class TestUrls(SimpleTestCase):

    def test_manage_post_url(self):
        url = reverse('core:manage')
        self.assertEqual(resolve(url).func.view_class, ManagePostListView)

    def test_create_post_url(self):
        url = reverse('core:create')
        self.assertEqual(resolve(url).func.view_class, PostCreateView)

    def test_edit_post_url(self):
        url = reverse('core:post_edit', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, PostUpdateView)

    def test_delete_post_url(self):
        url = reverse('core:post_delete', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, PostDeleteView)

    def test_blog_url(self):
        url = reverse('core:blog')
        self.assertEqual(resolve(url).func, blog)

    def test_post_detail_url(self):
        url = reverse('core:post_detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func, post_detail)

    def test_post_share_url(self):
        url = reverse('core:post_share', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func, post_share)
