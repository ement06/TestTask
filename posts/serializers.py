from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from users.models import User

from .models import Post, Like

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ['user_id']
    

    def create(self, **kwargs):
        like = Like(**kwargs)
        like.save()
        return like
    
    def delete(self, **kwargs):
        like = Like.objects.filter(user_id=kwargs['user_id'], post_id=kwargs['post_id']).first()
        like.delete()
        return like


    @staticmethod
    def get_post_by_id(id):
        try:
            post = Post.objects.get(id=id)
        except ObjectDoesNotExist:
            return None
        return post


    @staticmethod
    def get_data(validated_data):
        user = User.objects.get(email=validated_data['user_email'])
        return user


class PostSerializer(serializers.ModelSerializer):
    
    id = serializers.IntegerField()
    title = serializers.CharField(required=True)
    body = serializers.CharField()
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    count_like = serializers.SerializerMethodField(method_name='likes', read_only=True)
    likes_data = LikeSerializer(many=True)

    class Meta:
        model = Post
        fields =['id', 'title', 'body', 'user_id', 'count_like', 'likes_data']
    
    def likes(self, obj):
        res = Like.objects.filter(post_id=obj.id).count()
        return res

    def create(self, validated_data):
        email = validated_data['user_email']
        user = User.objects.get(email=email)
        title = validated_data['title']
        body = validated_data['body']
        post = Post(title=title, body=body, user_id=user)
        post.save()
        return post

    @staticmethod
    def get_data(validated_data):
        user = User.objects.get(email=validated_data['user_email'])
        responce = Post.objects.filter(user_id=user.id)
        return responce
