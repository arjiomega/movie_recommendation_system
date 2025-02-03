from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import CustomUserSerializer
from django.contrib.auth import get_user_model

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenRefreshView

from users.models import UserMovie
from movies.models import MovieInfo

class CustomTokenRefreshView(TokenRefreshView):
    pass

# User Registration API
class RegisterUser(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Login API
class LoginUser(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access for login

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = get_user_model().objects.get(email=email)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response(
                    {
                        "message": "Login successful", 
                        "user": {"username": user.username},
                        "access_token": access_token,  # Send the access token
                        "refresh_token": str(refresh)  # Optional: You can send refresh token if needed
                    }, status=status.HTTP_200_OK
                )
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except get_user_model().DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
class UserMovieView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Only logged-in users can access

    def get(self, request):
        user_movies = UserMovie.objects.filter(user_id=request.user)  # Fetch movies for the logged-in user
        data = [
            {
                "movie_id": um.movie_id.movie_id,
                "movie_title": um.movie_id.title,
                "rating": um.rating,
                "review": um.review
            }
            for um in user_movies
        ]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        """Allow users to rate and review movies"""
        user = request.user  # Get the logged-in user
        movie_id = request.data.get("movie_id")
        rating = request.data.get("rating")
        review = request.data.get("review", "")

        try:
            movie = MovieInfo.objects.get(movie_id=movie_id)
        except MovieInfo.DoesNotExist:
            return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)

        # Create or update UserMovie record
        user_movie, created = UserMovie.objects.update_or_create(
            user_id=user, movie_id=movie,
            defaults={"rating": rating, "review": review}
        )

        return Response({"message": "Rating submitted successfully"}, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        """Allow users to delete their movie rating and review"""
        user = request.user  # Get the logged-in user
        movie_id = request.data.get("movie_id")

        try:
            movie = MovieInfo.objects.get(movie_id=movie_id)
        except MovieInfo.DoesNotExist:
            return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            user_movie = UserMovie.objects.get(user_id=user, movie_id=movie)
            user_movie.delete()
            return Response({"message": "Rating deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except UserMovie.DoesNotExist:
            return Response({"error": "Rating not found"}, status=status.HTTP_404_NOT_FOUND)