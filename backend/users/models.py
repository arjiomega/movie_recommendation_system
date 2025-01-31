from django.contrib.auth.models import AbstractUser
from django.db import models

SCHEMA_NAME = "app"

# Custom User Model
class CustomUser(AbstractUser):
    avatar_path = models.URLField(blank=True, null=True)  # Optional profile picture URL
    email = models.EmailField(unique=True)  # Add unique constraint to email

    class Meta:
        db_table = f'"{SCHEMA_NAME}"."custom_user"'  # Store in specific schema

# Movie Model
class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    release_year = models.PositiveIntegerField()

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = f'"{SCHEMA_NAME}"."movie"'  # Store in specific schema

    def save(self, *args, **kwargs):
        # Automatically generate username from email if not provided
        if not self.username:
            self.username = self.email.split('@')[0]  # Set username to part before @ in email
        super().save(*args, **kwargs)

# User-Movie Relationship Model (Tracks movies watched, ratings, and reviews)
class UserMovie(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Many users can watch many movies
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)  # Many movies can be watched by many users
    rating = models.PositiveSmallIntegerField(blank=True, null=True)  # Optional rating (e.g., 1-5)
    review = models.TextField(blank=True, null=True)  # Optional review

    class Meta:
        unique_together = ('user', 'movie')  # Ensures a user can only rate a movie once
        db_table = f'"{SCHEMA_NAME}"."user_movie"'  # Store in specific schema

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} ({self.rating}/5)"
