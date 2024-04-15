from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from .models import Movie, Actor, Award, Director, Studio, Purchase
from .forms import (MovieForm, AddActorForm, AddMovieForm, ActorForm, AwardForm, DirectorForm, 
                    StudioForm, PurchaseForm, AwardGetForm, MovieReportForm)
from .serializers import MovieSerializer
from rest_framework import generics
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.db.models import Count
from django.contrib.auth.models import User
from django.db.models import Sum, Count

def is_admin(request):
    return request.user.groups.filter(name='admin').exists()

UNAUTHORIZED_REDIRECT = 'unauthorized'

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

        context = {'kdramas':kdramas, "kdrama_grouping":kdrama_group, 'is_admin':is_admin(request)}

        return render(request = request, template_name=self.template_name, context=context)

class MovieDetailView(LoginRequiredMixin, View):
    template_name = 'kdrama/movie_details.html'

    def get(self, request, kdrama_id=None):
        if kdrama_id:
            kdrama = Movie.objects.get(movie_id=kdrama_id)
        else:
            kdrama = Movie()
        
        context = {'kdrama':kdrama, 'movie_id':kdrama_id, 'is_admin':is_admin(request)}

        return render(request = request, template_name=self.template_name, context=context)
    
class MovieAddActorView(LoginRequiredMixin, View):
    template_name = 'kdrama/movie_add_actor.html'
    action = "Add Actor to "
    object = 'Actor'

    def get(self, request, kdrama_id=None):
        if not is_admin(request):
            return redirect(reverse(UNAUTHORIZED_REDIRECT))
        
        if kdrama_id:
            kdrama = Movie.objects.get(movie_id=kdrama_id)
        else:
            kdrama = Movie()

        form = AddActorForm()
        
        context = {'subject':self.action + kdrama.title, 'form':form, 'object':self.object, 'is_admin':is_admin(request)}

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
        
        context = {'subject':self.action + kdrama.title, 'form':form, 'object':self.object, 'is_admin':is_admin(request)}

        return render(request = request, template_name=self.template_name, context=context)
    
class MovieRemoveActorView(LoginRequiredMixin, View):
    template_name = 'kdrama/movie_remove_actor.html'

    def get(self, request, kdrama_id=None):
        if not is_admin(request):
            return redirect(reverse(UNAUTHORIZED_REDIRECT))
        
        if kdrama_id:
            kdrama = Movie.objects.get(movie_id=kdrama_id)
        else:
            kdrama = Movie()

        form = AddActorForm()
        form.fields['actor_selection'].queryset = kdrama.actors
        
        context = {'kdrama':kdrama, 'form':form, 'is_admin':is_admin(request)}

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
        
        context = {'kdrama':kdrama, 'form':kdrama_form, 'is_admin':is_admin(request)}

        return render(request = request, template_name=self.template_name, context=context)

class MovieCreateView(LoginRequiredMixin, View):
    template_name = 'kdrama/movie_form.html'
    action = "Add"

    def get(self, request):
        if not is_admin(request):
            return redirect(reverse(UNAUTHORIZED_REDIRECT))

        kdrama_form = MovieForm()

        context = {'form':kdrama_form, 'action':self.action, 'is_admin':is_admin(request)}

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
        
        context = {'form':kdrama_form, 'action':self.action, 'is_admin':is_admin(request)}

        return render(request = request, template_name=self.template_name, context=context)


class MovieUpdateView(LoginRequiredMixin, View):
    template_name = 'kdrama/movie_form.html'
    action = "Update"

    def get(self, request, kdrama_id=None):
        if not is_admin(request):
            return redirect(reverse(UNAUTHORIZED_REDIRECT))
        
        if kdrama_id:
            kdrama = Movie.objects.get(movie_id=kdrama_id)
        else:
            kdrama = Movie()

        kdrama_form = MovieForm(instance=kdrama)
        
        context = {'kdrama':kdrama, 'form':kdrama_form, 'action':self.action, 'is_admin':is_admin(request)}

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
        
        context = {'kdrama':kdrama, 'form':kdrama_form, 'action':self.action, 'is_admin':is_admin(request)}

        return render(request = request, template_name=self.template_name, context=context)

class MovieDeleteView(LoginRequiredMixin, View):
    template_name = 'kdrama/movie_form.html'
    action = "Delete"

    def get(self, request, kdrama_id=None):
        if not is_admin(request):
            return redirect(reverse(UNAUTHORIZED_REDIRECT))
        
        if kdrama_id:
            kdrama = Movie.objects.get(movie_id=kdrama_id)
        else:
            kdrama = Movie()

        kdrama_form = MovieForm(instance=kdrama)
        
        for field in kdrama_form.fields:
            kdrama_form.fields[field].widget.attrs['disabled'] = True

        context = {'kdrama':kdrama, 'form':kdrama_form, 'action':self.action, 'is_admin':is_admin(request)}

        return render(request = request, template_name=self.template_name, context=context)
    
    def post(self, request, kdrama_id=None):

        kdrama = Movie.objects.get(movie_id=kdrama_id)
        
        kdrama.delete()
            
        return redirect(reverse('movie-list'))
    
class ActorListView(LoginRequiredMixin, View):
    template_name = 'actors/actor_list.html'

    def get(self, request):
        actors = Actor.objects.all()

        context = {'actors':actors, 'is_admin':is_admin(request)}

        return render(request, self.template_name, context)
    
class ActorAddMovieView(LoginRequiredMixin, View):
    template_name = 'kdrama/movie_add_actor.html'
    action = "Add K-Drama to "
    object = 'K-Drama'

    def get(self, request, actor_id=None):
        if not is_admin(request):
            return redirect(reverse(UNAUTHORIZED_REDIRECT))
        
        if actor_id:
            actor = Actor.objects.get(actor_id=actor_id)
        else:
            actor = Actor()

        form = AddMovieForm()
        
        context = {'subject':self.action + str(actor), 'form':form, 'object':self.object, 'is_admin':is_admin(request)}

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
        
        context = {'subject':self.action + str(actor), 'form':form, 'object':self.object, 'is_admin':is_admin(request)}

        return render(request = request, template_name=self.template_name, context=context)

class ActorCreateView(LoginRequiredMixin, View):
    template_name = 'actors/actor_form.html'
    action = "Add"

    def get(self, request):
        if not is_admin(request):
            return redirect(reverse(UNAUTHORIZED_REDIRECT))
        
        actor_form = ActorForm()
        context = {'form': actor_form, 'action': self.action, 'is_admin':is_admin(request)}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        actor_form = ActorForm(request.POST)
        if actor_form.is_valid():
            actor_form.save()

            return redirect(reverse('actor-list'))
        
        context = {'form': actor_form, 'action': self.action, 'is_admin':is_admin(request)}

        return render(request, template_name=self.template_name, context=context)

class ActorDetailView(LoginRequiredMixin, View):
    template_name = 'actors/actor_details.html'

    def get(self, request, actor_id=None):
        if actor_id:
            actor = Actor.objects.get(actor_id=actor_id)
        else:
            actor = Actor()

        kdramas = Movie.objects.filter(actors=actor)

        context = {'actor':actor, 'kdramas':kdramas, 'is_admin':is_admin(request)}

        return render(request, self.template_name, context=context)

class ActorUpdateView(LoginRequiredMixin, View):
    template_name = 'actors/actor_form.html'
    action = "Update"

    def get(self, request, actor_id):
        if not is_admin(request):
            return redirect(reverse(UNAUTHORIZED_REDIRECT))
        
        actor = get_object_or_404(Actor, pk=actor_id)
        actor_form = ActorForm(instance=actor)
        context = {'form': actor_form, 'action': self.action, 'is_admin':is_admin(request)}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, actor_id):
        actor = get_object_or_404(Actor, pk=actor_id)
        actor_form = ActorForm(request.POST, instance=actor)
        if actor_form.is_valid():
            actor_form.save()
            return redirect(reverse('actor-list'))
        context = {'form': actor_form, 'action': self.action, 'is_admin':is_admin(request)}
        return render(request, template_name=self.template_name, context=context)


class ActorDeleteView(LoginRequiredMixin, View):
    template_name = "actors/actor_form.html"
    action = "Delete"

    def get(self, request, actor_id):
        if not is_admin(request):
            return redirect(reverse(UNAUTHORIZED_REDIRECT))
        
        actor = get_object_or_404(Actor, pk=actor_id)

        actor_form = ActorForm(instance=actor)

        for field in actor_form.fields:
            actor_form.fields[field].widget.attrs['disabled'] = True

        context = {'form':actor_form, 'action':'Delete', 'is_admin':is_admin(request)}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, actor_id):
        actor = get_object_or_404(Actor, pk=actor_id)
        actor.delete()
        return redirect(reverse('actor-list'))

class AwardCreateView(LoginRequiredMixin, View):
    template_name = 'awards/award_form.html'
    action = "Add"

    def get(self, request, movie_id):
        if not is_admin(request):
            return redirect(reverse(UNAUTHORIZED_REDIRECT))

        kdrama = get_object_or_404(Movie, pk=movie_id)

        form = AwardForm()
        context = {'form': form, 'kdrama':kdrama, 'action':self.action, 'is_admin':is_admin(request)}
        return render(request, self.template_name, context)

    def post(self, request, movie_id):
        kdrama = get_object_or_404(Movie, pk=movie_id)

        form = AwardForm(request.POST)
        if form.is_valid():
            award = form.save(commit=False)
            award.save()
            
            kdrama.awards.add(award)
            return redirect(reverse('movie-details') + str(movie_id))
        
        context = {'form': form, 'kdrama':kdrama, 'action':self.action, 'is_admin':is_admin(request)}
        return render(request, self.template_name, context)

class AwardUpdateView(LoginRequiredMixin, View):
    template_name = 'awards/award_form.html'
    action = "Update"

    def get(self, request, movie_id, award_id):
        if not is_admin(request):
            return redirect(reverse(UNAUTHORIZED_REDIRECT))
        
        kdrama = get_object_or_404(Movie, pk=movie_id)
        award = get_object_or_404(Award, pk=award_id)

        form = AwardForm(instance=award)
        context = {'form': form, 'kdrama':kdrama, 'action':self.action, 'is_admin':is_admin(request)}
        return render(request, self.template_name, context)

    def post(self, request, movie_id, award_id):
        kdrama = get_object_or_404(Movie, pk=movie_id)
        award = get_object_or_404(Award, pk=award_id)

        form = AwardForm(request.POST, instance=award)
        if form.is_valid():
            award = form.save(commit=False)
            award.save()
            
            return redirect(reverse('movie-details') + str(movie_id))
        
        context = {'form': form, 'kdrama':kdrama, 'action':self.action, 'is_admin':is_admin(request)}
        return render(request, self.template_name, context)

class AwardDeleteView(LoginRequiredMixin, View):
    template_name = 'awards/award_form.html'
    action = 'Delete'

    def get(self, request, movie_id):
        if not is_admin(request):
            return redirect(reverse(UNAUTHORIZED_REDIRECT))
        
        kdrama = get_object_or_404(Movie, pk=movie_id)
        form = AwardGetForm()
        form.fields['award'].queryset = kdrama.awards

        context = {'form': form, 'action':self.action, 'is_admin':is_admin(request)}
        return render(request, self.template_name, context)

    def post(self, request, movie_id):
        kdrama = get_object_or_404(Movie, pk=movie_id)
        form = AwardGetForm(request.POST)
        form.fields['award'].queryset = kdrama.awards

        if form.is_valid():
            award = form.cleaned_data.get('award')
            award.delete()

        return redirect(reverse('movie-details') + str(movie_id))
    
class ReportHomeView(LoginRequiredMixin, View):
    template_name = 'reports/report_home.html'

    def get(self, request):
        if not is_admin(request):
            return redirect(reverse(UNAUTHORIZED_REDIRECT))

        context = {'is_admin':is_admin(request)}

        return render(request, self.template_name, context)
    
class CustomerSalesReportView(LoginRequiredMixin, View):
    template_name = 'reports/customer_sales.html'

    def get(self, request):
        if not is_admin(request):
            return redirect(reverse(UNAUTHORIZED_REDIRECT))

        user_list = Purchase.objects.values('user__username').annotate(total_sales=Sum('total'), num_orders=Count('purchase_id'))
        user_list = sorted(user_list, key=lambda x: x['total_sales'], reverse=True)

        context = {'users':user_list, 'is_admin':is_admin(request)}
        
        return render(request, self.template_name, context)

class MovieSalesReportView(LoginRequiredMixin, View):
    template_name = 'reports/movie_sales.html'

    def get(self, request):
        if not is_admin(request):
            return redirect(reverse(UNAUTHORIZED_REDIRECT))

        form = MovieReportForm()

        context = {'form':form, 'is_admin':is_admin(request)}
        
        return render(request, self.template_name, context)
    
    def post(self, request):

        form = MovieReportForm(request.POST)

        if form.is_valid():
            kdrama = form.cleaned_data.get('kdrama')
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')

            kdrama_stats = Purchase.objects.filter(movie=kdrama, purchase_date__range=(start_date, end_date))
            total_revenue = kdrama_stats.aggregate(total_revenue=Sum('total'))['total_revenue']
            num_orders = kdrama_stats.aggregate(num_orders=Count('purchase_id'))['num_orders']

            total_revenue = total_revenue if total_revenue != None else 0

            context = {'form':form, 'kdrama':kdrama, 'num_orders':num_orders, 'total_revenue':total_revenue, 'is_admin':is_admin(request)}
        else:
            context = {'form':form, 'is_admin':is_admin(request)}
        
        return render(request, self.template_name, context)

class MovieActorListReportView(LoginRequiredMixin, View):
    template_name = 'reports/actor_list.html'

    def get(self, request):
        if not is_admin(request):
            return redirect(reverse(UNAUTHORIZED_REDIRECT))

        form = PurchaseForm()

        context = {'form':form, 'is_admin':is_admin(request)}
        
        return render(request, self.template_name, context)
    
    def post(self, request):

        form = PurchaseForm(request.POST)

        if form.is_valid():
            kdrama = form.cleaned_data.get('kdrama')

            context = {'form':form, 'kdrama':kdrama, 'is_admin':is_admin(request)}
        else:
            context = {'form':form, 'is_admin':is_admin(request)}
        
        return render(request, self.template_name, context)

class MovieAwardListReportView(LoginRequiredMixin, View):
    template_name = 'reports/movie_awards.html'

    def get(self, request):
        if not is_admin(request):
            return redirect(reverse(UNAUTHORIZED_REDIRECT))

        kdramas = Movie.objects.exclude(awards__isnull=True)
        context = {'kdramas':kdramas, 'is_admin':is_admin(request)}
        
        return render(request, self.template_name, context)

# Director Views
class DirectorListView(LoginRequiredMixin, View):
    template_name = 'directors/director_list.html'

    def get(self, request):
        directors = Director.objects.all()

        context = {'directors':directors, 'is_admin':is_admin(request)}

        return render(request, self.template_name, context)

class DirectorDetailView(LoginRequiredMixin, View):
    template_name = 'directors/director_details.html'

    def get(self, request, director_id=None):
        if director_id:
            director = Director.objects.get(director_id=director_id)
        else:
            director = Director()

        kdramas = Movie.objects.filter(director=director)

        context = {'director':director, 'kdramas':kdramas, 'is_admin':is_admin(request)}

        return render(request, self.template_name, context=context)

class DirectorCreateView(LoginRequiredMixin, View):
    template_name = 'directors/director_form.html'
    action = "Add"

    def get(self, request):
        if not is_admin(request):
            return redirect(reverse(UNAUTHORIZED_REDIRECT))
        
        director_form = DirectorForm()
        context = {'form': director_form, 'action': self.action, 'is_admin':is_admin(request)}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        director_form = DirectorForm(request.POST)
        if director_form.is_valid():
            director_form.save()

            return redirect(reverse('director-list'))
        
        context = {'form': director_form, 'action': self.action, 'is_admin':is_admin(request)}

        return render(request, template_name=self.template_name, context=context)

class DirectorUpdateView(LoginRequiredMixin, View):
    template_name = 'directors/director_form.html'
    action = "Update"

    def get(self, request, director_id):
        if not is_admin(request):
            return redirect(reverse(UNAUTHORIZED_REDIRECT))
        
        director = get_object_or_404(Director, pk=director_id)
        director_form = DirectorForm(instance=director)
        context = {'form': director_form, 'action': self.action, 'is_admin':is_admin(request)}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, director_id):
        director = get_object_or_404(Director, pk=director_id)
        director_form = DirectorForm(request.POST, instance=director)
        if director_form.is_valid():
            director_form.save()
            return redirect(reverse('director-details') + str(director_id))
        context = {'form': director_form, 'action': self.action, 'is_admin':is_admin(request)}
        return render(request, template_name=self.template_name, context=context)


class DirectorDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "directors/director_form.html"
    action = "Delete"

    def get(self, request, director_id):
        if not is_admin(request):
            return redirect(reverse(UNAUTHORIZED_REDIRECT))
        
        director = get_object_or_404(Director, pk=director_id)

        director_form = DirectorForm(instance=director)

        for field in director_form.fields:
            director_form.fields[field].widget.attrs['disabled'] = True

        context = {'form':director_form, 'action':'Delete', 'is_admin':is_admin(request)}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, director_id):
        director = get_object_or_404(Director, pk=director_id)
        director.delete()
        return redirect(reverse('director-list'))

# Studio Views
class StudioListView(LoginRequiredMixin, View):
    template_name = 'studio/studio_list.html'

    def get(self, request):
        studios = Studio.objects.all()

        context = {'studios':studios, 'is_admin':is_admin(request)}

        return render(request, self.template_name, context)

class StudioCreateView(LoginRequiredMixin, View):
    template_name = 'studio/studio_form.html'
    action = "Add"

    def get(self, request):
        if not is_admin(request):
            return redirect(reverse(UNAUTHORIZED_REDIRECT))
        
        studio_form = StudioForm()
        context = {'form': studio_form, 'action': self.action, 'is_admin':is_admin(request)}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        studio_form = StudioForm(request.POST)
        if studio_form.is_valid():
            studio_form.save()

            return redirect(reverse('studio-list'))
        
        context = {'form': studio_form, 'action': self.action, 'is_admin':is_admin(request)}

        return render(request, template_name=self.template_name, context=context)

class StudioDetailView(LoginRequiredMixin, View):
    template_name = 'studio/studio_details.html'

    def get(self, request, studio_id=None):
        if studio_id:
            studio = Studio.objects.get(studio_id=studio_id)
        else:
            studio = Studio()

        kdramas = Movie.objects.filter(studio=studio)

        context = {'studio':studio, 'kdramas':kdramas, 'is_admin':is_admin(request)}

        return render(request, self.template_name, context=context)

class StudioUpdateView(LoginRequiredMixin, View):
    template_name = 'studio/studio_form.html'
    action = "Update"

    def get(self, request, studio_id):
        if not is_admin(request):
            return redirect(reverse(UNAUTHORIZED_REDIRECT))
        
        studio = get_object_or_404(Studio, pk=studio_id)
        studio_form = StudioForm(instance=studio)
        context = {'form': studio_form, 'action': self.action, 'is_admin':is_admin(request)}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, studio_id):
        studio = get_object_or_404(Studio, pk=studio_id)
        studio_form = StudioForm(request.POST, instance=studio)
        if studio_form.is_valid():
            studio_form.save()
            return redirect(reverse('studio-details') + str(studio_id))
        context = {'form': studio_form, 'action': self.action, 'is_admin':is_admin(request)}
        return render(request, template_name=self.template_name, context=context)


class StudioDeleteView(LoginRequiredMixin, View):
    template_name = "studio/studio_form.html"
    action = "Delete"

    def get(self, request, studio_id):
        if not is_admin(request):
            return redirect(reverse(UNAUTHORIZED_REDIRECT))
        
        studio = get_object_or_404(Studio, pk=studio_id)

        studio_form = StudioForm(instance=studio)

        for field in studio_form.fields:
            studio_form.fields[field].widget.attrs['disabled'] = True

        context = {'form':studio_form, 'action':'Delete', 'is_admin':is_admin(request)}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, studio_id):
        studio = get_object_or_404(Studio, pk=studio_id)
        studio.delete()
        return redirect(reverse('studio-list'))


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
        
        context = {'kdrama':kdrama, 'form':kdrama_form, 'is_admin':is_admin(request)}

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
        
        context = {'order':order, 'is_admin':is_admin(request)}

        return render(request = request, template_name=self.template_name, context=context)
    
class UserPurchasesView(LoginRequiredMixin, View):
    template_name = 'kdrama/view_purchases.html'

    def get(self, request):
        purchases = Purchase.objects.filter(user=request.user)
        
        context = {'purchases':purchases, 'is_admin':is_admin(request)}

        return render(request = request, template_name=self.template_name, context=context)

class Unauthorized(LoginRequiredMixin, View):
    template_name = 'registration/unauthorized.html'

    def get(self, request):
        
        context = {'is_admin':is_admin(request)}

        return render(request = request, template_name=self.template_name, context=context)