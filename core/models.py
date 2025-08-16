#from django.db import models

# Create your models here.
# core/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser # We'll use Django's built-in User system, but make it better!

# 1. Our Super User Blueprint (like a special ID card for each user)
class User(AbstractUser):
    # We can add more fields later if we want, like a profile picture!
    # For now, Django's AbstractUser gives us username, password, email, etc.
    pass

# 2. Our Post Blueprint (what people share)
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Who made the post? If the user disappears, their posts disappear too.
    content = models.TextField() # The actual text of the post
    created_at = models.DateTimeField(auto_now_add=True) # When was it posted? Automatically set!

    def __str__(self):
        return f"Post by {self.user.username} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

# 3. Our Comment Blueprint (what people say about posts)
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # Which post is this comment for?
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Who made the comment?
    content = models.TextField() # The actual text of the comment
    created_at = models.DateTimeField(auto_now_add=True) # When was it commented?

    def __str__(self):
        return f"Comment by {self.user.username} on Post {self.post.id}"

# 4. Our Like Blueprint (who liked what)
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # Which post was liked?
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Who liked it?
    created_at = models.DateTimeField(auto_now_add=True) # When was it liked?

    class Meta:
        unique_together = ('post', 'user') # A user can only like a post once!

    def __str__(self):
        return f"Like by {self.user.username} on Post {self.post.id}"

# 5. Our Follow Blueprint (who follows whom)
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE) # The person who is following
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE) # The person being followed
    created_at = models.DateTimeField(auto_now_add=True) # When did they start following?

    class Meta:
        unique_together = ('follower', 'followed') # A user can only follow another user once!

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"
