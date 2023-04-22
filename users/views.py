from rest_framework.views import APIView, Request, Response, status
from users.models import User
from users.serializers import UserSerializer
from rest_framework.pagination import PageNumberPagination
import ipdb


class UserView(APIView, PageNumberPagination):
    def get(self, request: Request) -> Response:
        users = User.objects.all()
        result_page = self.paginate_queryset(users, request)
        serializer = UserSerializer(result_page, many=True)

        return self.paginate_queryset(serializer.data, status.HTTP_200_OK)

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
