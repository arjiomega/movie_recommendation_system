import requests
from django.http import JsonResponse

def get_popular_movies(request):
    url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TOKEN}"  # Replace with your actual TMDB token
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        return JsonResponse({"error": "Failed to fetch data"}, status=500)
