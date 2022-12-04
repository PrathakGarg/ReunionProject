from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, Post, Comment


# Added username in JWT token for easier access in frontend
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token


# Register new user
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


# Get formatted user details with followers and following count
class UserSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'following', 'followers']
        extra_kwargs = {'following': {'read_only': True}, 'followers': {'read_only': True}}

    def get_following(self, obj):
        return obj.following.count()

    def get_followers(self, obj):
        return obj.followers.count()


# Create and serialize new comment
class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment']
        extra_kwargs = {'comment': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment


# Get formatted comment
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['user', 'comment', 'created_at']
        extra_kwargs = {'user': {'read_only': True}}

    def get_user(self, obj):
        return obj.user.username


# Get formatted post with comments
class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'desc', 'created_at', 'comments', 'likes']
        extra_kwargs = {'user': {'read_only': True}, 'created_at': {'read_only': True}}

    def get_likes(self, obj):
        return obj.likes.count()

    def get_comments(self, obj):
        comments = obj.comments.all()
        return CommentSerializer(comments, many=True).data
