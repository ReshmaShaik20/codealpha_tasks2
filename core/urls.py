# MySocialApp/core/urls.py
from django.urls import path
from . import views # Import our views from the same folder
from django.contrib.auth import views as auth_views # Django's built-in auth views

urlpatterns = [
    path('', views.home_view, name='home'), # Our home page
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'), # Using our custom login view
    path('logout/', views.logout_view, name='logout'), # Using our custom logout view

    # Social media features
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_detail_view, name='post_detail'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/unlike/', views.unlike_post, name='unlike_post'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/follow/', views.follow_user, name='follow_user'),
    path('profile/<str:username>/unfollow/', views.unfollow_user, name='unfollow_user'),
]
