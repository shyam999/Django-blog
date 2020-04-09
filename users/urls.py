from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    #registration urls
    path('register/', views.register, name='register'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),

    #authentication urls
    path('accounts/login/', auth_views.LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='authentication/logged_out.html'), name='logout'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='authentication/change-password.html'), name='change-password'),
    path('change-password-done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/change-password-done.html'), name='change-password-done'),

    #profile management urls
    re_path(r'^profile/(?P<username>[-_\w.]+)/$', views.profile, name='profile'),
    re_path(r'^profile/(?P<username>[-_\w.]+)/edit/$', views.profile_settings, name='profile_settings'),
]