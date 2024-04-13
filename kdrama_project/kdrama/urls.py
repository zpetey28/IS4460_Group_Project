from django.urls import path
from django.contrib.auth.views import LoginView
from .views import (MovieListView, MovieDetailView, MovieCreateView, 
                    MovieUpdateView, MovieDeleteView, MovieListCreateAPIView, 
                    MovieRetrieveUpdateDestroyAPIView, ActorListView, ActorCreateView, 
                    ActorDeleteView, ActorUpdateView, AwardListView, AwardDeleteView, 
                    AwardCreateView, AwardUpdateView, ActorDetailView, MovieAddActorView,
                    MovieRemoveActorView)


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
    path('actors/list', ActorListView.as_view(), name='actor-list'),
    path('actor/add', ActorCreateView.as_view(), name='actor-add'),
    path('actor/details/<int:actor_id>/', ActorDetailView.as_view(), name='actor-details'),
    path('actor/update/<int:actor_id>/', ActorUpdateView.as_view(), name='actor-update'),
    path('actor/delete/<int:actor_id>/', ActorDeleteView.as_view(), name='actor-delete'),

    path('details/<int:kdrama_id>/add-actor/', MovieAddActorView.as_view(), name='movie-add-actor'),
    path('details/<int:kdrama_id>/remove-actor/', MovieRemoveActorView.as_view(), name='movie-remove-actor'),

    #Award urls
    path('movie/<int:movie_id>/awards/', AwardListView.as_view(), name='movie-awards-list'),
    path('movie/<int:movie_id>/awards/add/', AwardCreateView.as_view(), name='movie-award-add'),
    path('movie/<int:movie_id>/awards/<int:award_id>/update/', AwardUpdateView.as_view(), name='movie-award-update'),
    path('movie/<int:movie_id>/awards/<int:award_id>/delete/', AwardDeleteView.as_view(), name='movie-award-delete'),
    
    
]