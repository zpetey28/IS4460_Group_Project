from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Movie
from .forms import MovieForm
from .serializers import MovieSerializer
from rest_framework import generics
from django.views import View
from .models import Movie
from .forms import MovieForm
from django.contrib.auth.mixins import LoginRequiredMixin


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

    def get(self, request):
        kdrama_form = MovieForm()

        context = {'form':kdrama_form}

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
        
        context = {'form':kdrama_form}

        return render(request = request, template_name=self.template_name, context=context)


class MovieUpdateView(LoginRequiredMixin, View):
    template_name = 'kdrama/movie_form.html'

    def get(self, request, kdrama_id=None):
        if kdrama_id:
            kdrama = Movie.objects.get(movie_id=kdrama_id)
        else:
            kdrama = Movie()

        kdrama_form = MovieForm(instance=kdrama)
        
        context = {'kdrama':kdrama, 'form':kdrama_form}

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
        
        context = {'kdrama':kdrama, 'form':kdrama_form}

        return render(request = request, template_name=self.template_name, context=context)

class MovieDeleteView(LoginRequiredMixin, View):
    template_name = 'kdrama/movie_form.html'

    def get(self, request, kdrama_id=None):
        if kdrama_id:
            kdrama = Movie.objects.get(movie_id=kdrama_id)
        else:
            kdrama = Movie()

        kdrama_form = MovieForm(instance=kdrama)
        
        for field in kdrama_form.fields:
            kdrama_form.fields[field].widget.attrs['disabled'] = True

        context = {'kdrama':kdrama, 'form':kdrama_form}

        return render(request = request, template_name=self.template_name, context=context)
    
    def post(self, request, kdrama_id=None):

        kdrama = Movie.objects.get(movie_id=kdrama_id)
        
        kdrama.delete()
            
        return redirect(reverse('movie-list'))