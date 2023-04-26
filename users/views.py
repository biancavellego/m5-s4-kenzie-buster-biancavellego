from rest_framework.views import APIView, Request, Response, status
from django.shortcuts import get_object_or_404
from users.models import User
from users.serializers import UserSerializer
from users.permissions import IsOwnerOrEmployee
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import CustomJWTSerializer
from rest_framework.pagination import PageNumberPagination
import ipdb


class LoginJWTView(TokenObtainPairView):
    serializer_class = CustomJWTSerializer


class UserView(APIView, PageNumberPagination):
    def get(self, request: Request) -> Response:
        users = User.objects.all()
        result_page = self.paginate_queryset(users, request)
        serializer = UserSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # It's possible to omit these steps and do them in the serializer:
        # user = User.objects.create_user(**serializer.validated_data)
        # serializer = UserSerializer(user)

        # But it will be necessary to apply .save() method in order to
        # trigger "def create" at serializers.py:
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrEmployee]

    def get(self, request: Request, user_id: int) -> Response:
        # 1st Search user:
        user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, user)
        # Since there's no request, no need to serialize the input data.
        # But the output data must be serialized:
        serializer = UserSerializer(instance=user)

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, user_id: int) -> Response:
        # 1st - Searching for user:
        user = get_object_or_404(User, id=user_id)
        # 2nd - Accessing has_object_permissions:
        self.check_object_permissions(request, user)
        # 3rd - Serializing input data:
        # OBS: To differentiate between the .save() from create, we need to add
        # the user instance inside the serializer:
        serializer = UserSerializer(instance=user, data=request.data, partial=True)
        # 4th - Verifying if data is valid:
        serializer.is_valid(raise_exception=True)
        # 5th -> To be continued at users.serializers.py
        # ...
        # 8th - Saving modifications (this save method is from rest_framework):
        serializer.save()
        # 9th - Serializing output data:
        serializer = UserSerializer(instance=user)

        return Response(serializer.data, status.HTTP_200_OK)
