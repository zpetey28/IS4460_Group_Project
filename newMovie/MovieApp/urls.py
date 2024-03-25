# myproject/urls.py (Assuming your Django project is named myproject)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('newMovie.urls')),  # Assuming your app is named MovieApp
]