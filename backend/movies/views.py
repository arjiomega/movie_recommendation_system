from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.core.paginator import Paginator
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

@api_view(['GET'])  # Allow only GET requests
def get_top_movies_paginated_view(request):
    # Get the page number from the query parameters (default to page 1)
    page_number = request.GET.get('page', 1)
    movie_per_page = request.GET.get('movie_per_page', 10)

    # Get the top N movies
    movies = MovieStatistics.get_top_movies()

    # Set up pagination, displaying 10 movies per page
    paginator = Paginator(movies, movie_per_page)  # Show 10 movies per page
    page_obj = paginator.get_page(page_number)
    
    # Return paginated data
    return JsonResponse({
        'top_movies': list(page_obj),  # Convert the page object to a list
        'page': page_obj.number,       # Current page number
        'total_pages': paginator.num_pages,  # Total number of pages
    }, safe=False)