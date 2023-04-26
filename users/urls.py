from django.urls import path
from users.views import UserView, UserDetailView, LoginJWTView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("users/", UserView.as_view()),
    path("users/login/", LoginJWTView.as_view()),
    path("users/<int:user_id>/", UserDetailView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
]
