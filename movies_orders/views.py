from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from movies_orders.serializers import MovieOrderSerializer
from users.models import User
from movies.models import Movie
from movies_orders.models import MovieOrder


class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # movie_orders = MovieOrder.objects.filter(movie=movie_object)
    # serializer = MovieOrderSerializer(movie_orders, many=True)
    # serializer.is_valid(raise_exception=True)
    def post(self, request: Request, movie_id: int) -> Response:
        movie_object = get_object_or_404(Movie, pk=movie_id)
        serializer = MovieOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(movie=movie_object, order=request.user)

        return Response(serializer.data, status.HTTP_201_CREATED)
