# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q # For searching later if we add it
from .models import User, Post, Comment, Like, Follow
from django.contrib import messages # To show success/error messages

# --- Authentication Views ---

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome!')
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required # Only logged-in users can access this!
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

# --- Social Media Core Views ---

@login_required
def home_view(request):
    # Fetch all posts, ordered by creation date (newest first)
    posts = Post.objects.all().order_by('-created_at')
    # To show if the current user liked a post (for the button logic)
    for post in posts:
        post.user_liked = Like.objects.filter(post=post, user=request.user).exists()
    return render(request, 'core/home.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Post.objects.create(user=request.user, content=content)
            messages.success(request, 'Your post has been shared!')
        else:
            messages.error(request, 'Post content cannot be empty.')
    return redirect('home')

@login_required
def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Check if the current user has liked this specific post
    post.user_liked = Like.objects.filter(post=post, user=request.user).exists()
    return render(request, 'core/post_detail.html', {'post': post})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, user=request.user, content=content)
            messages.success(request, 'Your comment has been added!')
        else:
            messages.error(request, 'Comment cannot be empty.')
    return redirect('post_detail', post_id=post.id)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    Like.objects.get_or_create(post=post, user=request.user) # Create if it doesn't exist
    messages.success(request, 'You liked this post!')
    # Redirect back to where the user came from, or home if not available
    return redirect(request.META.get('HTTP_REFERER', reverse('home')))

@login_required
def unlike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    Like.objects.filter(post=post, user=request.user).delete() # Delete the like
    messages.info(request, 'You unliked this post.')
    return redirect(request.META.get('HTTP_REFERER', reverse('home')))

@login_required
def profile_view(request, username):
    view_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=view_user).order_by('-created_at')
    is_following = Follow.objects.filter(follower=request.user, followed=view_user).exists()

    # To show if the current user liked a post on the profile page
    for post in posts:
        post.user_liked = Like.objects.filter(post=post, user=request.user).exists()

    return render(request, 'core/profile.html', {
        'view_user': view_user,
        'posts': posts,
        'is_following': is_following
    })

@login_required
def follow_user(request, username):
    followed_user = get_object_or_404(User, username=username)
    if request.user != followed_user: # Cannot follow yourself
        Follow.objects.get_or_create(follower=request.user, followed=followed_user)
        messages.success(request, f'You are now following {followed_user.username}!')
    else:
        messages.warning(request, "You cannot follow yourself.")
    return redirect('profile', username=username)

@login_required
def unfollow_user(request, username):
    followed_user = get_object_or_404(User, username=username)
    if request.user != followed_user: # Cannot unfollow yourself if you never followed
        Follow.objects.filter(follower=request.user, followed=followed_user).delete()
        messages.info(request, f'You unfollowed {followed_user.username}.')
    return redirect('profile', username=username)
