from rest_framework import serializers
from movies_orders.models import MovieOrder


class MovieOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(source="movie.title", read_only=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    buyed_by = serializers.CharField(source="order.email", read_only=True)
    buyed_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data: dict) -> MovieOrder:
        # Receives user(order) + movie:
        return MovieOrder.objects.create(**validated_data)
