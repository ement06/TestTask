from django.urls import path

from .views import PostView, PostOwnerView, LikeView

urlpatterns = [
    path('post/<int:pk>', PostView.as_view()),
    path('post', PostOwnerView.as_view()),
    path('like/<int:pk>', LikeView.as_view())
]