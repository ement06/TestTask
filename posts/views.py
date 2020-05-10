import jwt
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
    serializer_class = PostSerializer
    queryset = Post.objects
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

class LikeGenericView(generics.ListCreateAPIView):
    serializer_class = LikeSerializer
    queryset = Like.objects
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class LikeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LikeSerializer
    queryset = Like.objects
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)


class AnalystView(generics.ListAPIView):
    serializer_class = AnalystSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        date_from = datetime.strptime(self.request.query_params['date_from'], '%Y-%m-%d').replace(tzinfo=timezone.utc)
        date_to = datetime.strptime(self.request.query_params['date_to'], '%Y-%m-%d').replace(tzinfo=timezone.utc)
        queryset = Like.objects.filter(date__range=[date_from, date_to])
        return queryset
    