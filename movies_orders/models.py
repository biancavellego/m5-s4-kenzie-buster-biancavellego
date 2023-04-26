from django.db import models


# OBS:
# It would not be necessary to add the custom pivot table to INSTALLED_APPS if
# MovieOrder model was already inside the movies file (which is registered in INSTALLED_APPS).
# 1:N => User - MovieOrder
# 1:N => Movie - MovieOrder
class MovieOrder(models.Model):
    movie = models.ForeignKey(
        "movies.Movie",
        on_delete=models.CASCADE,
        related_name="movies_orders",
    )

    # order represents the user who made the order
    order = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="user_movies_orders",
    )

    buyed_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __repr__(self) -> str:
        return f"<MovieOrder: ({self.id}) - {self.buyed_at} - {self.price}>"
