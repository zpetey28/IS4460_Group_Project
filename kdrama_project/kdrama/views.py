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
    
class MovieAwardsReportView(ListView):
    model = Movie
    template_name = 'movie_awards_report.html'

    def get_queryset(self):
        return super().get_queryset().filter(awards__isnull=False).prefetch_related('awards')

'''
class TopSalesReportView(ListView):
    model = Customer
    template_name = 'top_sales_report.html'
    context_object_name = 'top_customers'

    def get_queryset(self):
        return super().get_queryset().annotate(total_sales=Count('sales')).order_by('-total_sales')[:10]'''

class DramaActorsReportView(ListView):
    model = Movie
    template_name = 'drama_actors_report.html'

    def get_queryset(self):
        self.movie = get_object_or_404(Movie, id=self.kwargs['movie_id'])
        return self.movie.actors.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie'] = self.movie
        return context
    
'''class DramaSalesOverTimeReportView(ListView):
    model = Sale
    template_name = 'drama_sales_over_time_report.html'
    context_object_name = 'sales'

    def get_queryset(self):
        self.movie_id = self.kwargs['movie_id']
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        return super().get_queryset().filter(movie_id=self.movie_id, date__range=(start_date, end_date))'''

# Director Views
class DirectorListView(LoginRequiredMixin, ListView):
    model = Director
    template_name = 'directors/director_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Directors List'
        context['description'] = 'View all directors here.'
        return context

class DirectorCreateView(LoginRequiredMixin, CreateView):
    model = Director
    form_class = DirectorForm
    template_name = 'directors/director_form.html'
    success_url = reverse_lazy('director-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Director'
        context['description'] = 'Enter details to add a new director.'
        return context

class DirectorUpdateView(LoginRequiredMixin, UpdateView):
    model = Director
    form_class = DirectorForm
    template_name = 'directors/director_form.html'
    success_url = reverse_lazy('director-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Director'
        context['description'] = 'Update director details.'
        return context

class DirectorDeleteView(LoginRequiredMixin, DeleteView):
    model = Director
    template_name = 'directors/director_confirm_delete.html'
    success_url = reverse_lazy('director-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Director'
        context['description'] = 'Confirm deletion of this director.'
        return context

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