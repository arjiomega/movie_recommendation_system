import datetime
from dateutil.relativedelta import relativedelta

from django.db import models
from django.db.models import F


class MovieInfo(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=500)
    original_title = models.CharField(max_length=500, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    original_language = models.CharField(max_length=10, null=True, blank=True)
    adult = models.BooleanField(default=False)
    video = models.BooleanField(default=False)
    backdrop_path = models.CharField(max_length=500, null=True, blank=True)
    poster_path = models.CharField(max_length=500, null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    homepage = models.URLField(null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    tagline = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        managed = False
        db_table = '"dw_movies"."dim_movie_info"'

class MovieStatistics(models.Model):
    movie_id = models.OneToOneField(
        MovieInfo, 
        on_delete=models.CASCADE, 
        db_column="movie_id", 
        primary_key=True
    )
    vote_count = models.IntegerField(null=True, blank=True)
    vote_average = models.FloatField(null=True, blank=True)
    popularity = models.FloatField(null=True, blank=True)
    total_reviews = models.IntegerField(null=True, blank=True)
    budget = models.BigIntegerField(null=True, blank=True)
    revenue = models.BigIntegerField(null=True, blank=True)
    runtime = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = '"dw_movies"."fact_movie_statistics"'

    @classmethod
    def get_top_10_movies(cls):
        today = datetime.date.today()
        one_month_ago = today - relativedelta(months=2)
        get_top_N = 12

        movies = (
            MovieInfo.objects
            .filter(release_date__range=[one_month_ago, today])
            .annotate(popularity=F('moviestatistics__popularity'))
            .order_by('-popularity')
            .values("movie_id", "title", "release_date", "popularity", "backdrop_path", "poster_path")[:get_top_N]
        )

        return list(movies)