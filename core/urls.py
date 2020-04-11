from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.blog, name='blog'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('<int:pk>/share/', views.post_share, name='post_share'),

    path('manage/', views.ManagePostListView.as_view(), name='manage'),
    path('create/', views.PostCreateView.as_view(), name='create'),
    path('<pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('<pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]