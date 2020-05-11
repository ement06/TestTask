"""Post views."""

from datetime import datetime, timezone

from rest_framework import generics
from rest_framework import permissions

from .models import Post, Like
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    PostSerializer,
    LikeSerializer,
    AnalystSerializer,
)


class PostGenericView(generics.ListCreateAPIView):
    """Post list create view."""

    serializer_class = PostSerializer
    queryset = Post.objects
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Post detail view."""

    serializer_class = PostSerializer
    queryset = Post.objects
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)


class LikeGenericView(generics.ListCreateAPIView):
    """Like list create view."""

    serializer_class = LikeSerializer
    queryset = Like.objects
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        """Saves like to post.

        Args:
            serializer (LikeSerializer obj):

        """

        serializer.save(user_id=self.request.user)


class LikeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Like retrieve update destroy view."""

    serializer_class = LikeSerializer
    queryset = Like.objects
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)


class AnalystView(generics.ListAPIView):
    """Analyst list view."""

    serializer_class = AnalystSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        """Forms queryset for getting likes by date."""

        date_from = datetime.strptime(self.request.query_params['date_from'], '%Y-%m-%d').replace(tzinfo=timezone.utc)
        date_to = datetime.strptime(self.request.query_params['date_to'], '%Y-%m-%d').replace(tzinfo=timezone.utc)
        queryset = Like.objects.filter(date__range=[date_from, date_to])
        return queryset
