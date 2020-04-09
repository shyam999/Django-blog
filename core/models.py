from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from users.models import UserProfile

class Category(models.Model):
    
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:post_list_by_category', args=[self.slug])


class Post(models.Model):

    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='posts/%Y/%m/%d', blank=True, null = True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name = "Author")
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now, verbose_name = "creation date")

    class Meta:
        ordering = ['title',]
        index_together = (('id'),)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:post_detail', args=[self.pk])

class Subscribe(models.Model):

    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email