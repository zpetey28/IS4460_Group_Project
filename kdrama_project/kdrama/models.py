import sys
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Award(models.Model):
    award_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Studio(models.Model):
    studio_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    founded = models.DateField()
    owner = models.CharField(max_length=100)


    def __str__(self):
        return self.name

class Actor(models.Model):
    actor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    image_url = models.URLField(blank=True, max_length=sys.maxsize)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Director(models.Model):
    director_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    image_url = models.URLField(blank=True, max_length=sys.maxsize)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)
    director = models.ForeignKey(Director, on_delete=models.CASCADE,default=1)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE,default=1)
    release_year = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    episode_length = models.IntegerField(blank=True, null=True) # runtime in minutes
    seasons = models.IntegerField(default=1, null=True)
    episodes = models.IntegerField(default=1, null=True)
    rating = models.CharField(max_length=50, blank=True)
    genre = models.CharField(max_length=50, blank=True)
    image_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    actors = models.ManyToManyField('Actor', related_name='movies')
    awards = models.ManyToManyField('Award', related_name='movies')

    def __str__(self):
        return self.title
    
class Purchase(models.Model):
    purchase_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(default=datetime.now)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"