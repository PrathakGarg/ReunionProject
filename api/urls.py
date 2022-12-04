from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    MyTokenObtainPairView,
    register,
    follow_user,
    unfollow_user,
    get_user,
    create_post,
    get_or_delete_post,
    like_post,
    unlike_post,
    comment_post,
    get_posts,
)

urlpatterns = [
    path('authenticate/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register, name='register'),
    path('follow/<int:id>/', follow_user, name='follow_user'),
    path('follow/', follow_user, name='follow_user'),
    path('unfollow/<int:id>/', unfollow_user, name='unfollow_user'),
    path('unfollow/', unfollow_user, name='unfollow_user'),
    path('user/', get_user, name='get_user'),
    path('posts/', create_post, name='create_post'),
    path('posts/<int:id>/', get_or_delete_post, name='get_or_delete_post'),
    path('like/<int:id>/', like_post, name='like_post'),
    path('unlike/<int:id>/', unlike_post, name='unlike_post'),
    path('comment/<int:id>/', comment_post, name='comment_post'),
    path('all_posts/', get_posts, name='get_posts'),
]
