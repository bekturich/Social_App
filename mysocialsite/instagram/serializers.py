from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import UserProfile, Follow, Post, PostLike, Comment, CommentLike, Story, UserSave, \
    UserSaveItem
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'last_name', 'first_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Неверные учетные данные')

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username',]


class FollowSerializer(serializers.ModelSerializer):
    follower = UserProfileSimpleSerializer(read_only=True)
    following = UserProfileSimpleSerializer(read_only=True)
    created_at = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer(read_only=True)
    created_at = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))

    class Meta:
        model = Post
        fields = ['id', 'user', 'image', 'video', 'description', 'hashtag', 'created_at']


class PostLikeSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    created_at = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))
    class Meta:
        model = PostLike
        fields = ['id', 'user', 'post', 'like', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    created_at = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))
    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'text', 'parent', 'created_at',]


class CommentLikeSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer(read_only=True)
    comment = CommentSerializer(read_only=True)
    created_at = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))
    class Meta:
        model = CommentLike
        fields = ['id', 'user', 'comment', 'like', 'created_at']


class StorySerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer(read_only=True)
    created_at = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))
    class Meta:
        model = Story
        fields = ['id', 'user', 'image', 'video', 'created_at']


class UserSaveSerializer(serializers.ModelSerializer):
    # user = UserProfileSerializer(read_only=True)

    class Meta:
        model = UserSave
        fields = ['id', 'user']


class UserSaveItemSerializer(serializers.ModelSerializer):
    # save = SaveSerializer(read_only=True)
    # post = PostSerializer(read_only=True)

    class Meta:
        model = UserSaveItem
        fields = ['id', 'post', 'save', 'created_date']
