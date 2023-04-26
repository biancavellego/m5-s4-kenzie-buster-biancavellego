from django.db import models
from movies_orders.models import MovieOrder


class Rating(models.TextChoices):
    Rated_G = "G"
    Rated__PG = "PG"
    Rated_PG_13 = "PG-13"
    Rated_R = "R"
    Rated_NC_17 = "NC-17"


class Movie(models.Model):
    title = models.CharField(max_length=127)
    duration = models.CharField(max_length=10, null=True, default=None)
    rating = models.CharField(
        max_length=20, choices=Rating.choices, default=Rating.Rated_G
    )
    synopsis = models.TextField(null=True, default=None)

    # User -> Movie (1:N)
    # And on the "Many" side of the relationship we add the FK:
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="movies",
        # Optional: just explicitly declaring that a movie needs a user:
        null=False,
    )

    # Movie and User will have a ManyToMany relation:
    orders = models.ManyToManyField(
        "users.User",
        # Through which table this relation is happening (i.e. the custom pivot table):
        through="movies_orders.MovieOrder",
        related_name="ordered_movies",
    )

    def __repr__(self) -> str:
        return f"<Movie: ({self.id}) - {self.title} - {self.duration} - {self.rating} - {self.synopsis}>"
