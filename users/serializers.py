from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.views import User


class CustomJWTSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email

        return token


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, write_only=True)
    password = serializers.CharField(max_length=127, write_only=True)


# Code class (class that does almost everything):
class UserSerializer(serializers.Serializer):
    # id: Auto-created by the database:
    id = serializers.IntegerField(read_only=True)
    # Attributes inherited from AbstractUser:
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="username already taken.",
            ),
        ],
    )
    password = serializers.CharField(max_length=127, write_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    # Custom attributes:
    email = serializers.EmailField(
        required=True,
        max_length=127,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="email already registered.",
            )
        ],
    )
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthdate = serializers.DateField(allow_null=True, default=None)
    is_employee = serializers.BooleanField(allow_null=True, default=False)

    def validate(self, value):
        if value.get("is_employee", False):
            value["is_superuser"] = True
        else:
            value["is_superuser"] = False

        return value

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        # 6th - Updating (instance receives the new values for each key):
        for key, value in validated_data.items():
            if key == "password":
                # hashing password:
                instance.set_password(value)
            else:
                setattr(instance, key, value)

        # 7th - Saving the instance (this save method is from vanilla django
        # and references the model itself):
        instance.save()

        # 8th - Returning the instance:
        return instance
