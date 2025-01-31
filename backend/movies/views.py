from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.decorators import api_view

from .serializers import MovieInfoSerializer
from .models import MovieInfo, MovieStatistics

class MovieInfoViewSet(viewsets.ModelViewSet):
    queryset = MovieInfo.objects.all()
    serializer_class = MovieInfoSerializer
    http_method_names = ['get']  # Read-only API

@api_view(['GET'])  # Allow only GET requests
def get_top_10_movies_view(request):
    movies = MovieStatistics.get_top_10_movies()  # Call the class method
    return JsonResponse({'top_movies': movies}, safe=False)  # Return as JSON
