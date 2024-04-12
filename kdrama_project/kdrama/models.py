import sys
from django.db import models

class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)
    director = models.CharField(max_length=100, blank=True)
    release_year = models.CharField(max_length=50, blank=True)
    budget = models.CharField(max_length=50, blank=True)
    runtime = models.CharField(max_length=50, blank=True)
    rating = models.CharField(max_length=50, blank=True)
    genre = models.CharField(max_length=50, blank=True)
    image_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    actors = models.ManyToManyField('Actor', related_name='movies')
    awards = models.ManyToManyField('Award', related_name='movies')

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
    image_url = models.URLField(blank=True, default="https://i.pinimg.com/736x/c0/74/9b/c0749b7cc401421662ae901ec8f9f660.jpg", max_length=sys.maxsize)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class MovieCharacter(models.Model):
    character_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Director(models.Model):
    director_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
