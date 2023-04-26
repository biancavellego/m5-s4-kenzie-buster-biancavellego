from rest_framework import serializers
from movies.models import Movie, Rating


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10, allow_null=True, default=None)
    rating = serializers.ChoiceField(choices=Rating.choices, default=Rating.Rated_G)
    synopsis = serializers.CharField(allow_null=True, default=None)
    # If you'd like to add user on the response:
    # user = UserSerializer(read_only=True)

    # Adding a read_only field that will show a value you want:
    added_by = serializers.SerializerMethodField()

    def get_added_by(self, obj):
        return obj.user.email

    def create(self, validated_data: dict):
        return Movie.objects.create(**validated_data)
