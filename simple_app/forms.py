from django import forms
from .models import simpleModel

class simpleForm(forms.ModelForm):
    class Meta:
        model = simpleModel

        fields = [
            "title",
            "description",
        ]