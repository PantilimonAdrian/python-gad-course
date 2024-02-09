import datetime

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Choices for the platform where the game was played
PLATFORM_CHOICES = [
    ('PC', 'PC'),
    ('PlayStation', 'PlayStation'),
    ('Xbox', 'Xbox'),
    ('Nintendo', 'Nintendo'),
]

def current_year():
    """Function used to return the current year"""
    return datetime.date.today().year


def max_value_current_year(value):
    """Function used to determine current year as the maximum value"""
    return MaxValueValidator(current_year())(value)


class BaseModel(models.Model):
    """This class is the base model for all the other ORM models"""

    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class GameHistory(BaseModel):
    """This class is the model used to store information about
    each game played by an user."""

    # Each game history of a game is associated with only one user and
    # an user can have multiple game history for different games.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    hours_played = models.PositiveIntegerField(default=0)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    year_played = models.PositiveIntegerField(
        default=current_year(), validators=[MinValueValidator(1960), max_value_current_year]
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "gamehistory"
        constraints = [
            # Using question object Q we validate if the rating and chosen platform are correct
            models.CheckConstraint(check=models.Q(rating__gte=1) & models.Q(rating__lte=5), name='valid_rating'),
            models.CheckConstraint(check=models.Q(platform__in=[choice[0] for choice in PLATFORM_CHOICES]),
                                   name='valid_platform'),
            # Restrict that an there should be only one entry for an user and a game name
            models.UniqueConstraint(fields=['user', 'name'], name='unique_game_for_user')
        ]