from django.utils import timezone
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Category, Post, Subscribe
from django.contrib.auth.models import User
from users.models import UserProfile
from .forms import EmailPostForm, SubscribeForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class OwnerMixin(object):
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(author=self.request.user.userprofile)


class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user.userprofile
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerPostMixin(OwnerMixin, LoginRequiredMixin):
    model = Post
    fields = ['category', 'title', 'slug',
              'image', 'author', 'content', 'created_date']
    success_url = reverse_lazy('core:manage_post_list')


class OwnerPostEditMixin(OwnerPostMixin, OwnerEditMixin):
    fields = ['category', 'title', 'slug',
              'image', 'author', 'content', 'created_date']
    success_url = reverse_lazy('core:manage_post_list')
    template_name = 'core/manage/form.html'


class ManagePostListView(OwnerPostMixin, ListView):
    template_name = 'core/manage/list.html'


class PostCreateView(PermissionRequiredMixin, OwnerPostEditMixin, CreateView):
    permission_required = 'core.add_post'


class PostUpdateView(PermissionRequiredMixin, OwnerPostEditMixin, UpdateView):
    permission_required = 'core.change_post'


class PostDeleteView(PermissionRequiredMixin, OwnerPostMixin, DeleteView):
    template_name = 'core/manage/delete.html'
    success_url = reverse_lazy('core:manage_post_list')
    permission_required = 'core.delete_post'


def get_post_queryset(query=None):
    queryset = []
    queries = query.split(' ')
    for q in queries:
        posts = Post.objects.filter(
            Q(title__icontains=q) | Q(content__icontains=q)).distinct()
        for post in posts:
            queryset.append(post)
    return list(set(queryset))


def blog(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    posts = Post.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
    query = ''
    if request.GET:
        query = request.GET['q']
        query = str(query)
        posts = sorted(get_post_queryset(query), reverse=True)
    paginator = Paginator(posts, 4)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    form = SubscribeForm(request.POST or None)
    if request.method == 'POST':
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            posts = posts.filter(category=category)
        if form.is_valid():
            instance = form.save(commit=False)
            if Subscribe.objects.filter(email=instance.email).exists():
                print("user exists")
            else:
                instance.save()
    else:
        form = SubscribeForm()
    return render(request, 'core/display/post_list.html', {'category': category,
                                                           'categories': categories, 'posts': posts,
                                                           'query': query, 'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'core/display/post_detail.html', {'post': post})


def post_share(request, pk):
    post = get_object_or_404(Post, pk=pk)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(
                cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(
                post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'core/display/post_share.html', {'post': post, 'form': form, 'sent': sent})
