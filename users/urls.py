from django.urls import path
from users.views import UserView, LoginJWTView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("users/", UserView.as_view()),
    path("users/login/", LoginJWTView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
]
