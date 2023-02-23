from django import forms
from .models import UserRating

class userForm(forms.ModelForm):
    class Meta:
        model = UserRating

        fields = [
            "user",
            "movie_id",
            "rating"
        ]