from django.views import View
from .forms import UserRegistrationForm
from django.shortcuts import render, redirect
from django.urls import reverse

class RegisterView(View):
    template_name = 'registration/register.html'

    def get(self, request):
        form = UserRegistrationForm()
        context = {'form':form}
        return render(request, template_name=self.template_name, context=context)
    
    def post(self, request):
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
        
        context = {'form':form}
        return render(request, template_name=self.template_name, context=context)