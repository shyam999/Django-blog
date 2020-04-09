from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import UserRegistrationForm, UserProfileForm, ProfileEditForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from . models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = UserRegistrationForm()
        profile_form = UserProfileForm()
    return render(request, 'registration/register.html', {'form': form, 'profile_form': profile_form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    if not user:
        return redirect('users:register')
    profile = UserProfile.objects.get(user=user)
    context = {'username': username, 'user': user, 'profile': profile}
    return render(request, 'account/profile.html', context)

@login_required
def profile_settings(request, username):
    user = User.objects.get(username=username)
    profile = UserProfile.objects.get(user=user)
    if request.user != user:
        return redirect('users:home')
    if request.method == 'POST':
        print(request.POST)
        form = ProfileEditForm(request.POST, instance=user.userprofile, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('users:profile', kwargs={'username': user.username}))
    else:
        form = ProfileEditForm(instance=user.userprofile)
    context = {'user': user, 'form': form}
    return render(request, 'account/profile_edit.html', context)