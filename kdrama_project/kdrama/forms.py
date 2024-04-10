from django import forms
from .models import Movie, Actor

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'director', 'release_year', 'budget', 'runtime', 'rating', 'genre', 'image_url', 'youtube_url']

class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = ['first_name', 'last_name', 'date_of_birth']