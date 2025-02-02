from django.contrib.auth.models import AbstractUser
from django.db import models

from movies.models import MovieInfo  # Import the correct Movie model

SCHEMA_NAME = "app"

# Custom User Model
class CustomUser(AbstractUser):
    avatar_path = models.URLField(blank=True, null=True)  # Optional profile picture URL
    email = models.EmailField(unique=True)  # Add unique constraint to email

    class Meta:
        db_table = f'"{SCHEMA_NAME}"."custom_user"'  # Store in specific schema

# User-Movie Relationship Model (Tracks movies watched, ratings, and reviews)
class UserMovie(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column="user_id")  # Explicit column name
    movie_id = models.ForeignKey(MovieInfo, on_delete=models.CASCADE, to_field="movie_id", db_column="movie_id")
    rating = models.PositiveSmallIntegerField(blank=True, null=True)  # Optional rating (e.g., 1-5)
    review = models.TextField(blank=True, null=True)  # Optional review

    class Meta:
        unique_together = (('user_id', 'movie_id'),)  # Ensures a user can only rate a movie once
        db_table = f'"{SCHEMA_NAME}"."user_movie"'  # Store in specific schema

    def __str__(self):
        return f"{self.user_id.username} - {self.movie_id.title} ({self.rating}/5)"
