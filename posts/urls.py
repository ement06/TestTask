from django.urls import path

from .views import (
    PostGenericView,
    PostDetailView,
    LikeGenericView,
    LikeDetailView,
    AnalystView,
    )


urlpatterns = [
    path('', PostGenericView.as_view()),
    path('<int:pk>/', PostDetailView.as_view()),
    path('like/', LikeGenericView.as_view()),
    path('like/<int:pk>/', LikeDetailView.as_view()),
    path('analyst/', AnalystView.as_view())
]