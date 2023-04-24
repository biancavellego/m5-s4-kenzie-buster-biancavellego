from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.CharField(max_length=127, unique=True)
    first_name = models.EmailField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthdate = models.DateField(null=True)
    is_employee = models.BooleanField(null=True, default=False)

    # def __repr__(self) -> str:
    #     return f"<User: ({self.id}) - {self.email} - {self.first_name} - {self.last_name} - {self.birthdate} - {self.is_employee}>"
