# Django imports for views and HTTP responses
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseForbidden

# Authentication and permission related imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm

# Generic class-based view imports
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView, View
from django.views.decorators.csrf import csrf_protect

# URL utility imports
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

# Application specific imports for models, forms, and serializers
from .models import Movie
from .forms import MovieForm, CustomLoginForm
from .serializers import MovieSerializer

# Django REST framework import for generic views
from rest_framework import generics




# MovieLoginView for handling login
class MovieLoginView(LoginView):
    form_class = AuthenticationForm  # Utilizes Django's built-in authentication form
    template_name = 'movie_login.html'  # Specifies the template used for the login page
    #redirect_authenticated_user = True  # Redirects users who are already authenticated

    def get_success_url(self):
        # This method returns the URL to redirect to after a successful login
        return reverse_lazy('movie_list')  # Redirects to the 'movie_list' URL
    
    def form_valid(self, form):
        login(self.request, form.get_user())
        # You can add any custom session handling here
        return HttpResponseRedirect(self.get_success_url())

# MovieLogoutView for handling logout
class MovieLogoutView(LogoutView):
    next_page = reverse_lazy('movie_login')  # Redirects to the login page after logout

    @method_decorator(csrf_protect)  # Ensure CSRF protection is applied to this view
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            logout(request)
            return redirect(self.next_page)
        return super().dispatch(request, *args, **kwargs)


class GroupRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='IsLoggedIn').exists()

    def handle_no_permission(self):
        # Render the 'forbidden.html' template for forbidden access
        return render(self.request, 'forbidden.html', status=403)



#API
class MovieListCreateAPIView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


#MovieList
class MovieListView(TemplateView, LoginRequiredMixin):
    template_name = 'movie_list.html'
    login_url = '/login/'  # Redirect to login page if not authenticated
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movies'] = Movie.objects.all()
        return context

#CRUD
class MovieDetailView(GroupRequiredMixin, DetailView):
    model = Movie
    template_name = 'movie_details.html'
    context_object_name = 'movie'
    login_url = '/login/'  # Redirect to login page if not authenticated

class MovieCreateView(GroupRequiredMixin, CreateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movie_form.html'
    success_url = reverse_lazy('movie_list')
    login_url = '/login/'  # Redirect to login page if not authenticated

class MovieUpdateView(GroupRequiredMixin, UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movie_form.html'
    success_url = reverse_lazy('movie_list')
    login_url = '/login/'  # Redirect to login page if not authenticated

class MovieDeleteView(GroupRequiredMixin, DeleteView):
    model = Movie
    template_name = 'movie_delete.html'
    success_url = reverse_lazy('movie_list')
    login_url = '/login/'  # Redirect to login page if not authenticated