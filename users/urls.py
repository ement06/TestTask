from django.urls import path, include

from .views import registration_view, login_view, logout_view

urlpatterns = [
    # path('auth/', include('rest_auth.urls')),
    path('login', login_view),
    path('register', registration_view),
    path('logout', logout_view)

]