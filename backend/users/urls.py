from django.urls import path
from .views import RegisterUser, LoginUser, UserMovieView, CustomTokenRefreshView

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register_user'),
    path('login/', LoginUser.as_view(), name='login_user'),
    path("user-movies/", UserMovieView.as_view(), name="user-movie-list"),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
