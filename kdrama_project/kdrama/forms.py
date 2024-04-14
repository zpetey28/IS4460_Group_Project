from django import forms
from .models import Movie, Actor, Award

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'director', 'studio', 'price', 'runtime', 'rating', 'genre', 'image_url', 'youtube_url']

class AddActorForm(forms.ModelForm):
    actor_selection = forms.ModelChoiceField(queryset=Actor.objects.all())

    class Meta:
        model = Actor
        fields = ['actor_selection']

class AddMovieForm(forms.ModelForm):
    kdrama_selection = forms.ModelChoiceField(queryset=Movie.objects.all())

    class Meta:
        model = Movie
        fields = ['kdrama_selection']

class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = "__all__"

class AwardForm(forms.ModelForm):
    class Meta:
        model = Award
        fields = ['name']
