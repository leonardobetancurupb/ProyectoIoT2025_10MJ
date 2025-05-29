from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db import transaction

from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from .models import UserProfile
from sensors.models import Sensor

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

class RegisterView(SuccessMessageMixin, CreateView):
    template_name = 'registration/register.html'
    success_url = reverse_lazy('accounts:login')
    form_class = UserRegistrationForm
    success_message = "Your account has been created successfully. You can now log in."

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('landing:home')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Create a user profile
        UserProfile.objects.create(user=self.object)
        return response

@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'registration/logged_in.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sensors'] = Sensor.objects.filter(owner=self.request.user)
        return context

@method_decorator(login_required, name='dispatch')
class EditProfileView(SuccessMessageMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('accounts:profile')
    success_message = "Your profile has been updated successfully."
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.POST:
            context['user_form'] = UserUpdateForm(self.request.POST, instance=self.request.user)
            context['profile_form'] = ProfileUpdateForm(self.request.POST, 
                                                    instance=self.request.user.profile)
        else:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
            context['profile_form'] = ProfileUpdateForm(instance=self.request.user.profile)
            
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        profile_form = context['profile_form']
        
        with transaction.atomic():
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
            else:
                return self.form_invalid(form)
                
        return super().form_valid(form)