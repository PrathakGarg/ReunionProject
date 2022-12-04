from django.db import models
from django.contrib.auth.models import AbstractUser


# Custom user model with email as pk
class User(AbstractUser):
    email = models.EmailField(unique=True)

    # Implemented followers and following as ManyToMany relation of Users
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


# Post model connected to User model
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True, null=True)

    def __str__(self):
        return self.title


# Comment model connected to User and Post models
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment
