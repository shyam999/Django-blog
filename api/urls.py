from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.PostListView.as_view(), name="post_list"),
    path('<int:id>/', views.api_post_view, name="api_post_view"),
    path('create/', views.api_create_post_view, name="api_create_post"),
    path('<int:id>/update', views.api_update_post_view, name="api_update_post"),
    path('<int:id>/delete', views.api_delete_post_view, name="api_delete_post"),
]