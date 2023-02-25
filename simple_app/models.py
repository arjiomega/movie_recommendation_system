# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Ratings(models.Model):
    user_id = models.IntegerField()
    movie_id = models.IntegerField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    timestamp = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'ratings'


class MovieInfo(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    imdb_id = models.IntegerField()
    tmdb_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'movie_info'

class UserInfo(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        #managed = False
        db_table = 'user_info'


class UserRating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)

    class Meta:
        #managed = False
        db_table = 'user_rating'
        unique_together = (('user', 'movie_id'),)
