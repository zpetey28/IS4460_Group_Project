from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Movie
from .forms import MovieForm
from .serializers import MovieSerializer
from rest_framework import generics
from django.views import View
from .models import Movie, Actor
from .forms import MovieForm, ActorForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

class MovieListCreateAPIView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieListView(LoginRequiredMixin, View):
    template_name = 'kdrama/movie_list.html'

    def get(self, request):
        kdramas = Movie.objects.all()
        context = {'kdramas':kdramas}

        return render(request = request, template_name=self.template_name, context=context)

class MovieDetailView(LoginRequiredMixin, View):
    template_name = 'kdrama/movie_details.html'

    def get(self, request, kdrama_id=None):
        if kdrama_id:
            kdrama = Movie.objects.get(movie_id=kdrama_id)
        else:
            kdrama = Movie()
        
        context = {'kdrama':kdrama}

        return render(request = request, template_name=self.template_name, context=context)

class MovieCreateView(LoginRequiredMixin, View):
    template_name = 'kdrama/movie_form.html'
    action = "Add"

    def get(self, request):
        kdrama_form = MovieForm()

        context = {'form':kdrama_form, 'action':self.action}

        return render(request = request, template_name=self.template_name, context=context)
    
    def post(self, request, kdrama_id=None):
        if kdrama_id:
            kdrama = Movie.objects.get(movie_id=kdrama_id)
        else:
            kdrama = Movie()

        kdrama_form = MovieForm(request.POST, instance=kdrama)

        if kdrama_form.is_valid():
            
            kdrama_form.save()
            return redirect(reverse('movie-list'))
        
        context = {'form':kdrama_form, 'action':self.action}

        return render(request = request, template_name=self.template_name, context=context)


class MovieUpdateView(LoginRequiredMixin, View):
    template_name = 'kdrama/movie_form.html'
    action = "Update"

    def get(self, request, kdrama_id=None):
        if kdrama_id:
            kdrama = Movie.objects.get(movie_id=kdrama_id)
        else:
            kdrama = Movie()

        kdrama_form = MovieForm(instance=kdrama)
        
        context = {'kdrama':kdrama, 'form':kdrama_form, 'action':self.action}

        return render(request = request, template_name=self.template_name, context=context)
    
    def post(self, request, kdrama_id=None):
        if kdrama_id:
            kdrama = Movie.objects.get(movie_id=kdrama_id)
        else:
            kdrama = Movie()

        kdrama_form = MovieForm(request.POST, instance=kdrama)

        if kdrama_form.is_valid():
            
            kdrama_form.save()
            return redirect(reverse('movie-details') + str(kdrama_id))
        
        context = {'kdrama':kdrama, 'form':kdrama_form, 'action':self.action}

        return render(request = request, template_name=self.template_name, context=context)

class MovieDeleteView(LoginRequiredMixin, View):
    template_name = 'kdrama/movie_form.html'
    action = "Delete"

    def get(self, request, kdrama_id=None):
        if kdrama_id:
            kdrama = Movie.objects.get(movie_id=kdrama_id)
        else:
            kdrama = Movie()

        kdrama_form = MovieForm(instance=kdrama)
        
        for field in kdrama_form.fields:
            kdrama_form.fields[field].widget.attrs['disabled'] = True

        context = {'kdrama':kdrama, 'form':kdrama_form, 'action':self.action}

        return render(request = request, template_name=self.template_name, context=context)
    
    def post(self, request, kdrama_id=None):

        kdrama = Movie.objects.get(movie_id=kdrama_id)
        
        kdrama.delete()
            
        return redirect(reverse('movie-list'))
    
'''class ActorListView(View):
    template_name = 'actors/actor-list.html'

    def get(self, request, **kwargs):
        movie_id = kwargs.get('movie_id')
        actors = Actor.objects.all()
        context = {'actors': actors}
        return render(request, self.template_name, context)'''
class ActorListView(View):
    template_name = 'actors/actor_list.html'

    def get(self, request, movie_id=None):
        if movie_id is not None:
            movie = get_object_or_404(Movie, pk=movie_id)
            actors = movie.actors.all()
            context = {'actors': actors, 'movie': movie}
            return render(request, self.template_name, context)
        else:
            # Handle the case where movie_id is not provided
            return HttpResponse("Movie ID is required.")

'''class ActorCreateView(View):
    template_name = 'actors/actor_form.html'
    action = "Add"

    def get(self, request):
        actor_form = ActorForm()
        context = {'form': actor_form, 'action': self.action}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        actor_form = ActorForm(request.POST)
        if actor_form.is_valid():
            actor_form.save()
            return redirect(reverse('actor-list'))
        context = {'form': actor_form, 'action': self.action}
        return render(request, template_name=self.template_name, context=context)'''
class ActorCreateView(View):
    template_name = 'actors/actor_form.html'
    action = "Add"

    def get(self, request, movie_id):
        actor_form = ActorForm()
        context = {'form': actor_form, 'action': self.action, 'movie_id': movie_id}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, movie_id):
        actor_form = ActorForm(request.POST)
        if actor_form.is_valid():
            actor_form.save()
            # Redirect to the movie actors list page
            return redirect(reverse('movie-actors-list', kwargs={'movie_id': movie_id}))
        context = {'form': actor_form, 'action': self.action, 'movie_id': movie_id}
        return render(request, template_name=self.template_name, context=context)

class ActorUpdateView(View):
    template_name = 'actors/actor_form.html'
    action = "Update"

    def get(self, request, actor_id):
        actor = get_object_or_404(Actor, pk=actor_id)
        actor_form = ActorForm(instance=actor)
        context = {'form': actor_form, 'action': self.action}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, actor_id):
        actor = get_object_or_404(Actor, pk=actor_id)
        actor_form = ActorForm(request.POST, instance=actor)
        if actor_form.is_valid():
            actor_form.save()
            return redirect(reverse('actor-list'))
        context = {'form': actor_form, 'action': self.action}
        return render(request, template_name=self.template_name, context=context)

class ActorDeleteView(View):
    template_name = 'actors/actor_confirm_delete.html'

    def get(self, request, actor_id):
        actor = get_object_or_404(Actor, pk=actor_id)
        context = {'actor': actor}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, actor_id):
        actor = get_object_or_404(Actor, pk=actor_id)
        actor.delete()
        return redirect(reverse('actor-list'))
    
