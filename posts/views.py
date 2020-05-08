from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from .models import Post, Like
from .serializers import PostSerializer, LikeSerializer
import jwt
from users.models import User


def check_auth(func):
    def decode_jwt_token(self, request, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            decode_token = jwt.decode(token, 'secret')
        except jwt.InvalidTokenError:
            return Response('You are not authorized', status.HTTP_403_FORBIDDEN)
        request.data['user_email'] = decode_token['email']
        return func(self, request, **kwargs)
    return decode_jwt_token


class PostView(APIView):

    def get(self, request, pk):
        if pk:
            post = Post.objects.get(id=pk)
            res = PostSerializer(post)
            return Response(res.data, status.HTTP_200_OK)

        responce = Post.objects.all()
        res = PostSerializer(responce, many=True)
        return Response(res.data, status.HTTP_200_OK)


class PostOwnerView(APIView):

    @check_auth
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if not serializer.is_valid():
            return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response('Done', status.HTTP_201_CREATED)

    @check_auth
    def get(self, request):
        data = PostSerializer.get_data(request.data)
        response = PostSerializer(data, many=True)
        return Response(response.data, status.HTTP_200_OK)


class LikeView(APIView):

    @check_auth
    def post(self, request, pk):
        post = LikeSerializer.get_post_by_id(pk)
        if post:
            user = LikeSerializer.get_data(request.data)
            serializer = LikeSerializer()
            serializer.create(post_id=post, user_id=user)
            response = 'You are succesfuly liked post'
        else:
            response = 'Sorry, we dont have this post'
        return Response(response, status.HTTP_200_OK)
    
    @check_auth
    def delete(self, request, pk):
        post = LikeSerializer.get_post_by_id(pk)
        if post:
            user = LikeSerializer.get_data(request.data)
            serializer = LikeSerializer()
            serializer.delete(post_id=post, user_id=user)
            response = 'You are succesfuly unliked post'
        else:
            response = 'Sorry, we dont have this post'
        return Response(response, status.HTTP_200_OK)

    @check_auth
    def get(self, request, pk):
        # post = LikeSerializer.get_post_by_id(pk)
        post = True
        if post:
            # res = Like.objects.filter(post_id=pk).count()
            # response = LikeSerializer({'count_like': res})
            response = LikeSerializer(Like, context={'post_id': pk})
            return Response(response.data, status.HTTP_200_OK)
        return Response('=(', status.HTTP_400_BAD_REQUEST)