from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema

from .serializers import (
    MyTokenObtainPairSerializer,
    CreateUserSerializer,
    UserSerializer,
    CreatePostSerializer,
    PostSerializer,
    CreateCommentSerializer,
)

from .models import User, Post, Comment


# Create your views here.
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@swagger_auto_schema(method='post', request_body=CreateUserSerializer)
@api_view(['POST'])
def register(request):
    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request: Request, id: int):
    user = request.user
    user_to_follow = User.objects.filter(id=id)

    if not user_to_follow.exists():
        return Response({'message': 'User not found'}, status=400)

    user_to_follow = user_to_follow.first()
    if user_to_follow == user:
        return Response({'message': 'You cannot follow yourself'}, status=400)
    if user_to_follow in user.following.all():
        return Response({'message': 'You are already following this user'}, status=400)

    user.following.add(user_to_follow)
    user.save()
    return Response({"message": f'User {user_to_follow.username} followed successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request: Request, id: int):
    user = request.user
    user_to_unfollow = User.objects.filter(id=id)

    if not user_to_unfollow.exists():
        return Response({'message': 'User not found'}, status=400)

    user_to_unfollow = user_to_unfollow.first()
    if user_to_unfollow == user:
        return Response({'message': 'You cannot unfollow yourself'}, status=400)
    if user_to_unfollow not in user.following.all():
        return Response({'message': 'You are not following this user'}, status=400)

    user.following.remove(user_to_unfollow)
    user.save()
    return Response({"message": f'User {user_to_unfollow.username} unfollowed successfully'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request: Request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request: Request):
    user = request.user
    serializer = CreatePostSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=user)
        return Response(serializer.data)
    return Response({"message": "Post creation failed", "errors": serializer.errors}, status=400)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def get_or_delete_post(request: Request, id: int):
    if request.method == 'GET':
        post = Post.objects.filter(id=id)

        if not post.exists():
            return Response({'message': 'Post not found'}, status=404)

        post = post.first()
        serializer = PostSerializer(post, many=False)
        serializer_data = {
            "id": serializer.data['id'],
            "likes": serializer.data['likes'],
            "comments": len(serializer.data['comments']),
        }
        return Response(serializer_data)
    elif request.method == 'DELETE':
        user = request.user
        post = Post.objects.filter(id=id)

        if not post.exists():
            return Response({'message': 'Post not found'}, status=404)

        post = post.first()
        if post.user != user:
            return Response({'message': 'You cannot delete this post'}, status=400)

        post.delete()
        return Response({"message": f'Post {post.id} deleted successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request: Request, id: int):
    user = request.user
    post = Post.objects.filter(id=id)

    if not post.exists():
        return Response({'message': 'Post not found'}, status=404)

    post = post.first()
    if post.user == user:
        return Response({'message': 'You cannot like your own post'}, status=400)
    if post in user.liked_posts.all():
        return Response({'message': 'You have already liked this post'}, status=400)

    user.liked_posts.add(post)
    user.save()
    return Response({"message": f'Post {post.id} liked successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_post(request: Request, id: int):
    user = request.user
    post = Post.objects.filter(id=id)

    if not post.exists():
        return Response({'message': 'Post not found'}, status=404)

    post = post.first()
    if post.user == user:
        return Response({'message': 'You cannot unlike your own post'}, status=400)
    if post not in user.liked_posts.all():
        return Response({'message': 'You have not liked this post'}, status=400)

    user.liked_posts.remove(post)
    user.save()
    return Response({"message": f'Post {post.id} unliked successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_post(request: Request, id: int):
    user = request.user
    post = Post.objects.filter(id=id)

    if not post.exists():
        return Response({'message': 'Post not found'}, status=404)

    post = post.first()
    serializer = CreateCommentSerializer(data=request.data)

    if serializer.is_valid():
        comment = serializer.save(user=user, post=post)
        return Response({"cid": comment.id})
    return Response({"message": "Comment creation failed", "errors": serializer.errors}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_posts(request: Request):
    user = request.user
    posts = Post.objects.filter(user=user)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
