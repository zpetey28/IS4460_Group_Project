from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from .views import MovieListView, MovieDetailView, MovieCreateView, MovieUpdateView, MovieDeleteView, MovieListCreateAPIView, MovieRetrieveUpdateDestroyAPIView, ActorListView, ActorCreateView, ActorDeleteView, ActorUpdateView


urlpatterns = [
    path('list/', MovieListView.as_view(), name='movie-list'),
    path('details/<int:kdrama_id>/', MovieDetailView.as_view(), name='movie-details'),
    path('details/', MovieDetailView.as_view(), name='movie-details'),

    path('add/', MovieCreateView.as_view(), name='movie-add'),

    path('update/<int:kdrama_id>/', MovieUpdateView.as_view(), name='movie-update'),
    path('update/', MovieUpdateView.as_view(), name='movie-update'),

    path('delete/<int:kdrama_id>/', MovieDeleteView.as_view(), name='movie-delete'),
    path('delete/', MovieDeleteView.as_view(), name='movie-delete'),

    #API urls
    path('api/movies/', MovieListCreateAPIView.as_view(), name='movie-list-create'),
    path('api/movies/<int:pk>/', MovieRetrieveUpdateDestroyAPIView.as_view(), name='movie-retrieve-update-destroy'),

    #Actor urls
    path('movie/<int:movie_id>/actors/', ActorListView.as_view(), name='movie-actors-list'),
    path('movie/<int:movie_id>/actors/add/', ActorCreateView.as_view(), name='movie-actor-add'),
    path('movie/<int:movie_id>/actors/<int:actor_id>/update/', ActorUpdateView.as_view(), name='movie-actor-update'),
    path('movie/<int:movie_id>/actors/<int:actor_id>/delete/', ActorDeleteView.as_view(), name='movie-actor-delete'),
    
]