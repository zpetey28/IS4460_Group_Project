from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from .models import Movie, Actor, Award, Director, Studio, Purchase
from .forms import MovieForm, AddActorForm, AddMovieForm, ActorForm, AwardForm, DirectorForm, StudioForm, PurchaseForm
from .serializers import MovieSerializer
from rest_framework import generics
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.db.models import Count
from django.contrib.auth.models import User

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
    action = "Add Actor to "
    object = 'Actor'

    def get(self, request, kdrama_id=None):
        if kdrama_id:
            kdrama = Movie.objects.get(movie_id=kdrama_id)
        else:
            kdrama = Movie()

        form = AddActorForm()
        
        context = {'subject':self.action + kdrama.title, 'form':form, 'object':self.object}

        return render(request = request, template_name=self.template_name, context=context)
    
    def post(self, request, kdrama_id=None):
        if kdrama_id:
            kdrama = Movie.objects.get(movie_id=kdrama_id)
        else:
            kdrama = Movie()

        form = AddActorForm(request.POST, instance=kdrama)
        

        if form.is_valid():
            
            kdrama.actors.add(form.cleaned_data.get('actor_selection'))
            kdrama.save()
            return redirect(reverse('movie-details') + str(kdrama_id))
        
        context = {'subject':self.action + kdrama.title, 'form':form, 'object':self.object}

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
    
class ActorAddMovieView(LoginRequiredMixin, View):
    template_name = 'kdrama/movie_add_actor.html'
    action = "Add K-Drama to "
    object = 'K-Drama'

    def get(self, request, actor_id=None):
        if actor_id:
            actor = Actor.objects.get(actor_id=actor_id)
        else:
            actor = Actor()

        form = AddMovieForm()
        
        context = {'subject':self.action + str(actor), 'form':form, 'object':self.object}

        return render(request = request, template_name=self.template_name, context=context)
    
    def post(self, request, actor_id=None):
        if actor_id:
            actor = Actor.objects.get(actor_id=actor_id)
        else:
            actor = Actor()

        form = AddMovieForm(request.POST, instance=actor)

        if form.is_valid():
            kdrama = form.cleaned_data.get('kdrama_selection')

            kdrama.actors.add(actor)
            kdrama.save()
            return redirect(reverse('actor-details') + str(actor_id))
        
        context = {'subject':self.action + str(actor), 'form':form, 'object':self.object}

        return render(request = request, template_name=self.template_name, context=context)

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

        kdramas = Movie.objects.filter(actors=actor)

        context = {'actor':actor, 'kdramas':kdramas}

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

class DramaActorsListView(LoginRequiredMixin, ListView):
    model = Movie
    template_name = 'drama_actors_list.html'
    context_object_name = 'movie'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.movie_id = self.kwargs['movie_id']
        return queryset.filter(pk=self.movie_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'List of Actors in Drama'
        context['description'] = 'View all actors in this drama.'
        return context

class TopSalesReportView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'top_sales_report.html'
    context_object_name = 'top_users'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.annotate(total_sales=Count('purchase')).order_by('-total_sales')[:10]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Top Sales Report'
        context['description'] = 'View top users based on sales.'
        return context

class DramaAwardsReportView(LoginRequiredMixin, ListView):
    model = Movie
    template_name = 'movie_awards_report.html'
    context_object_name = 'movies'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(awards__isnull=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Movie Awards Report'
        context['description'] = 'View movies that have received awards.'
        return context

class SalesOverTimeReportView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = 'sales_over_time_report.html'
    context_object_name = 'purchases'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('purchase_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sales Over Time Report'
        context['description'] = 'View sales of movies over time.'
        return context

# Director Views
class DirectorListView(LoginRequiredMixin, View):
    template_name = 'directors/director_list.html'

    def get(self, request):
        directors = Director.objects.all()

        context = {'directors':directors}

        return render(request, self.template_name, context)

class DirectorDetailView(LoginRequiredMixin, View):
    template_name = 'directors/director_details.html'

    def get(self, request, director_id=None):
        if director_id:
            director = Director.objects.get(director_id=director_id)
        else:
            director = Director()

        kdramas = Movie.objects.filter(director=director)

        context = {'director':director, 'kdramas':kdramas}

        return render(request, self.template_name, context=context)

class DirectorCreateView(LoginRequiredMixin, View):
    template_name = 'directors/director_form.html'
    action = "Add"

    def get(self, request):
        director_form = DirectorForm()
        context = {'form': director_form, 'action': self.action}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        director_form = DirectorForm(request.POST)
        if director_form.is_valid():
            director_form.save()

            return redirect(reverse('director-list'))
        
        context = {'form': director_form, 'action': self.action}

        return render(request, template_name=self.template_name, context=context)

class DirectorUpdateView(LoginRequiredMixin, View):
    template_name = 'directors/director_form.html'
    action = "Update"

    def get(self, request, director_id):
        director = get_object_or_404(Director, pk=director_id)
        director_form = DirectorForm(instance=director)
        context = {'form': director_form, 'action': self.action}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, director_id):
        director = get_object_or_404(Director, pk=director_id)
        director_form = DirectorForm(request.POST, instance=director)
        if director_form.is_valid():
            director_form.save()
            return redirect(reverse('director-details') + str(director_id))
        context = {'form': director_form, 'action': self.action}
        return render(request, template_name=self.template_name, context=context)


class DirectorDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "directors/director_form.html"
    action = "Delete"

    def get(self, request, director_id):
        director = get_object_or_404(Director, pk=director_id)

        director_form = DirectorForm(instance=director)

        for field in director_form.fields:
            director_form.fields[field].widget.attrs['disabled'] = True

        context = {'form':director_form, 'action':'Delete'}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, director_id):
        director = get_object_or_404(Director, pk=director_id)
        director.delete()
        return redirect(reverse('director-list'))

# Studio Views
class StudioListView(LoginRequiredMixin, ListView):
    model = Studio
    template_name = 'studios/studio_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Studios List'
        context['description'] = 'View all studios here.'
        return context

class StudioCreateView(LoginRequiredMixin, CreateView):
    model = Studio
    form_class = StudioForm
    template_name = 'studios/studio_form.html'
    success_url = reverse_lazy('studio-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Studio'
        context['description'] = 'Enter details to add a new studio.'
        return context

class StudioUpdateView(LoginRequiredMixin, UpdateView):
    model = Studio
    form_class = StudioForm
    template_name = 'studios/studio_form.html'
    success_url = reverse_lazy('studio-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Studio'
        context['description'] = 'Update studio details.'
        return context

class StudioDeleteView(LoginRequiredMixin, DeleteView):
    model = Studio
    template_name = 'studios/studio_confirm_delete.html'
    success_url = reverse_lazy('studio-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Studio'
        context['description'] = 'Confirm deletion of this studio.'
        return context

# Purchase Views
class PurchaseCreateView(LoginRequiredMixin, View):
    template_name = 'kdrama/purchase_form.html'

    def get(self, request, kdrama_id=None):
        if kdrama_id:
            kdrama = Movie.objects.get(movie_id=kdrama_id)
        else:
            kdrama = Movie()

        kdrama_form = PurchaseForm(instance=kdrama, initial={'kdrama':kdrama})
        for field in kdrama_form.fields:
            kdrama_form.fields[field].widget.attrs['disabled'] = True
        
        context = {'kdrama':kdrama, 'form':kdrama_form}

        return render(request = request, template_name=self.template_name, context=context)
    
    def post(self, request, kdrama_id=None):
        if kdrama_id:
            kdrama = Movie.objects.get(movie_id=kdrama_id)
        else:
            kdrama = Movie()
        
        order = Purchase(user=request.user, movie=kdrama, total=kdrama.price)
        order.save()

        return redirect(reverse('purchase-confirmation') + str(order.purchase_id))
    
class PurchaseConfirmationView(LoginRequiredMixin, View):
    template_name = 'kdrama/purchase_confirmation.html'

    def get(self, request, purchase_id=None):
        if purchase_id:
            order = Purchase.objects.get(purchase_id=purchase_id)
        else:
            order = Purchase()
        
        context = {'order':order}

        return render(request = request, template_name=self.template_name, context=context)
    
class UserPurchasesView(LoginRequiredMixin, View):
    template_name = 'kdrama/view_purchases.html'

    def get(self, request):
        purchases = Purchase.objects.filter(user=request.user)
        
        context = {'purchases':purchases}

        return render(request = request, template_name=self.template_name, context=context)