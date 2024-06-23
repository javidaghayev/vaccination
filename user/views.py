from django.shortcuts import render
from user.forms import *
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import login as user_login, authenticate, logout as user_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required


def signup(request):
    form = SignUpForm(request.POST or None,request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            messages.success(request, f"Account created for {first_name} {last_name}")
            return HttpResponseRedirect(reverse('index'))
        messages.error(request, 'Please enter valid data!')
        return render(request, 'user/signup.html', {'form': form})
    context = {
        'form': form
    }

    return render(request, 'user/signup.html', context)



def login(request):
    form = LoginForm(request, request.POST)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                user_login(request, user)
                messages.success(request, 'Login successfully')
                return HttpResponseRedirect(reverse('index'))
            messages.error(request, 'Please valid data39!')
            return HttpResponseRedirect(reverse("user:login"))
        messages.error(request, 'Please valid data41!')
        return HttpResponseRedirect(reverse("user:login"))
    return render(request, 'user/login.html', {'form': form})


@login_required
def logout(request):
    user_logout(request)
    messages.success(request, 'logged out successfully ')
    return HttpResponseRedirect(reverse('user:login'))


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password changed successfully')
            return HttpResponseRedirect(reverse('index'))
        messages.error(request, 'please enter valid data')
        return render(request, 'user/change_password.html', {'form': form})

    context = {
        'form': ChangePasswordForm(request.user)
    }
    return render(request, 'user/change_password.html', context)


@login_required
def profile_view(request):
    context = {
        'user': request.user
    }
    return render(request, 'user/profile_view.html', context)


@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated Successfully')
            return HttpResponseRedirect(reverse('user:profile'))
        messages.error(request, 'Please enter valid data')
        return render(request, 'user/profile_update.html', {'form': form})

    context = {
        'form': ProfileUpdateForm(instance=request.user)
    }
    return render(request, 'user/profile_update.html', context)

