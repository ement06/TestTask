"""Contains serializers for Post."""

from rest_framework import serializers

from .models import Post, Like


class LikeSerializer(serializers.ModelSerializer):
    """Like serializer."""

    class Meta:
        model = Like
        fields = ["post_id", "user_id", "date"]
        read_only_fields = ['user_id', 'date']


class PostSerializer(serializers.ModelSerializer):
    """Post serializer."""

    count_like = serializers.SerializerMethodField(method_name='likes')

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'user_id', 'count_like']
        read_only_fields = ['user_id', 'count_like']

    def likes(self, obj):
        """Counts likes per post.

        Args:
            obj (Post obj): Post model.

        Returns:
            int: Counted likes per post.

        """

        res = obj.like_set.all().count()
        return res


class AnalystSerializer(serializers.ModelSerializer):
    """Analyst serializer."""

    class Meta:
        model = Like
        fields = ['id', 'user_id', 'post_id', 'date']
