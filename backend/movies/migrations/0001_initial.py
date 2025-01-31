# Generated by Django 5.1.4 on 2025-01-30 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MovieInfo',
            fields=[
                ('movie_id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=500)),
                ('original_title', models.CharField(blank=True, max_length=500, null=True)),
                ('release_date', models.DateField(blank=True, null=True)),
                ('original_language', models.CharField(blank=True, max_length=10, null=True)),
                ('adult', models.BooleanField(default=False)),
                ('video', models.BooleanField(default=False)),
                ('backdrop_path', models.CharField(blank=True, max_length=500, null=True)),
                ('poster_path', models.CharField(blank=True, max_length=500, null=True)),
                ('overview', models.TextField(blank=True, null=True)),
                ('homepage', models.URLField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('tagline', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'db_table': '"dw_movies"."dim_movie_info"',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MovieStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_count', models.IntegerField(blank=True, null=True)),
                ('vote_average', models.FloatField(blank=True, null=True)),
                ('popularity', models.FloatField(blank=True, null=True)),
                ('total_reviews', models.IntegerField(blank=True, null=True)),
                ('budget', models.BigIntegerField(blank=True, null=True)),
                ('revenue', models.BigIntegerField(blank=True, null=True)),
                ('runtime', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': '"dw_movies"."fact_movie_statistics"',
                'managed': False,
            },
        ),
    ]
