from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Movie
from .forms import MovieForm, AddActorForm
from .serializers import MovieSerializer
from rest_framework import generics
from django.views import View
from .models import Movie, Actor, Award
from .forms import MovieForm, ActorForm, AwardForm
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

        kdrama_group = []
        for i in range(0, len(kdramas), 5):
            kdrama_group.append(kdramas[i:i + 5])

        context = {'kdramas':kdramas, "kdrama_grouping":kdrama_group}

        return render(request = request, template_name=self.template_name, context=context)

class MovieDetailView(LoginRequiredMixin, View):
    template_name = 'kdrama/movie_details.html'

    def get(self, request, kdrama_id=None):
        if kdrama_id:
            kdrama = Movie.objects.get(movie_id=kdrama_id)
        else:
            kdrama = Movie()
        
        context = {'kdrama':kdrama, 'movie_id':kdrama_id}

        return render(request = request, template_name=self.template_name, context=context)
    
class MovieAddActorView(LoginRequiredMixin, View):
    template_name = 'kdrama/movie_add_actor.html'

    def get(self, request, kdrama_id=None):
        if kdrama_id:
            kdrama = Movie.objects.get(movie_id=kdrama_id)
        else:
            kdrama = Movie()

        form = AddActorForm()
        
        context = {'kdrama':kdrama, 'form':form}

        return render(request = request, template_name=self.template_name, context=context)
    
    def post(self, request, kdrama_id=None):
        if kdrama_id:
            kdrama = Movie.objects.get(movie_id=kdrama_id)
        else:
            kdrama = Movie()

        kdrama_form = AddActorForm(request.POST, instance=kdrama)
        

        if kdrama_form.is_valid():
            
            kdrama.actors.add(kdrama_form.cleaned_data.get('actor_selection'))
            kdrama.save()
            return redirect(reverse('movie-details') + str(kdrama_id))
        
        context = {'kdrama':kdrama, 'form':kdrama_form}

        return render(request = request, template_name=self.template_name, context=context)
    
class MovieRemoveActorView(LoginRequiredMixin, View):
    template_name = 'kdrama/movie_remove_actor.html'

    def get(self, request, kdrama_id=None):
        if kdrama_id:
            kdrama = Movie.objects.get(movie_id=kdrama_id)
        else:
            kdrama = Movie()

        form = AddActorForm()
        form.fields['actor_selection'].queryset = kdrama.actors
        
        context = {'kdrama':kdrama, 'form':form}

        return render(request = request, template_name=self.template_name, context=context)
    
    def post(self, request, kdrama_id=None):
        if kdrama_id:
            kdrama = Movie.objects.get(movie_id=kdrama_id)
        else:
            kdrama = Movie()

        kdrama_form = AddActorForm(request.POST, instance=kdrama)
        

        if kdrama_form.is_valid():
            
            kdrama.actors.remove(kdrama_form.cleaned_data.get('actor_selection'))
            kdrama.save()
            return redirect(reverse('movie-details') + str(kdrama_id))
        
        context = {'kdrama':kdrama, 'form':kdrama_form}

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
    
class ActorListView(LoginRequiredMixin, View):
    template_name = 'actors/actor_list.html'

    def get(self, request):
        actors = Actor.objects.all()

        context = {'actors':actors}

        return render(request, self.template_name, context)

class ActorCreateView(LoginRequiredMixin, View):
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

        return render(request, template_name=self.template_name, context=context)

class ActorDetailView(LoginRequiredMixin, View):
    template_name = 'actors/actor_details.html'

    def get(self, request, actor_id=None):
        if actor_id:
            actor = Actor.objects.get(actor_id=actor_id)
        else:
            actor = Actor()

        context = {'actor':actor}

        return render(request, self.template_name, context=context)

class ActorUpdateView(LoginRequiredMixin, View):
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


class ActorDeleteView(LoginRequiredMixin, View):
    template_name = "actors/actor_form.html"
    action = "Delete"

    def get(self, request, actor_id):
        actor = get_object_or_404(Actor, pk=actor_id)

        actor_form = ActorForm(instance=actor)

        for field in actor_form.fields:
            actor_form.fields[field].widget.attrs['disabled'] = True

        context = {'form':actor_form, 'action':'Delete'}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, actor_id):
        actor = get_object_or_404(Actor, pk=actor_id)
        actor.delete()
        return redirect(reverse('actor-list'))
    

class AwardListView(LoginRequiredMixin, View):
    template_name = 'awards/award_list.html'

    def get(self, request, movie_id=None):
        if movie_id is not None:
            movie = get_object_or_404(Movie, pk=movie_id)
            awards = movie.awards.all()
            context = {'awards': awards, 'movie': movie}
            return render(request, self.template_name, context)
        else:
            return HttpResponse("Movie ID is required.")

class AwardCreateView(LoginRequiredMixin, View):
    template_name = 'awards/award_form.html'

    def get(self, request, movie_id):
        form = AwardForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, movie_id):
        form = AwardForm(request.POST)
        if form.is_valid():
            award = form.save(commit=False)
            award.save()
            movie = get_object_or_404(Movie, pk=movie_id)
            movie.awards.add(award)
            return redirect('movie-awards-list', movie_id=movie_id)
        else:
            context = {'form': form}
            return render(request, self.template_name, context)

class AwardUpdateView(LoginRequiredMixin, View):
    template_name = 'awards/award_form.html'

    def get(self, request, movie_id, award_id):
        award = get_object_or_404(Award, pk=award_id)
        form = AwardForm(instance=award)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, movie_id, award_id):
        award = get_object_or_404(Award, pk=award_id)
        form = AwardForm(request.POST, instance=award)
        if form.is_valid():
            form.save()
            return redirect('movie-awards-list', movie_id=movie_id)
        else:
            context = {'form': form}
            return render(request, self.template_name, context)

class AwardDeleteView(LoginRequiredMixin, View):
    template_name = 'awards/award_confirm_delete.html'

    def get(self, request, movie_id, award_id):
        award = get_object_or_404(Award, pk=award_id)
        context = {'award': award}
        return render(request, self.template_name, context)

    def post(self, request, movie_id, award_id):
        award = get_object_or_404(Award, pk=award_id)
        award.delete()
        return redirect('movie-awards-list', movie_id=movie_id)