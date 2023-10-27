from .models import CustomUser, Roles
from .forms import CustomUserCreationForm, RoleForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, ListView, DetailView, DeleteView
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin





class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'home/register.html'
    success_url = reverse_lazy('home') 
    model = CustomUser
    success_message = "Registration successful. you can now log in."
    


    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('login')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)
    

    

class LogoutInterfaceView(LogoutView):
    template_name = 'home/logout.html'
    success_url = reverse_lazy('login')


class LoginInterfaceView(LoginView):
    template_name = 'home/login.html'
    success_url = reverse_lazy('home')


class HomeView(TemplateView):
    template_name = 'home/welcome.html'


class AuthorizedView(LoginRequiredMixin, TemplateView):
    template_name = 'home/authorized.html'
    login_url = '/login'


class UpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'home/register.html'
    success_url = 'home'
    form_class = CustomUserCreationForm
    
    success_message = "User updated successfully."



    def get(self, request, *args, **kwargs):
        print("user", type(request.user))

        pk = self.request.user.pk
        self.object = self.model.objects.get(pk=pk)
        form = CustomUserCreationForm(instance=self.object)
        return render(request, 'home/register.html', {"form": form})


    def form_valid(self, form):
        form.instance.user = self.request.user 
        form.save()
        return HttpResponseRedirect(self.get_success_url())



class RoleListView(LoginRequiredMixin, ListView):
    template_name = 'roles/role_list.html'
    login_url = '/login'
    model = Roles
    context_object_name = 'roles'


class RoleDetailView(LoginRequiredMixin, DetailView):
    template_name = 'roles/role_detail.html'
    login_url = '/login'
    model = Roles
    context_object_name = 'role'

class RoleCreateView(LoginRequiredMixin, CreateView):
    template_name = 'roles/role_create.html'
    login_url = '/login'
    form_class = RoleForm
    success_url = reverse_lazy('roles')
    model = Roles

    def get(self, request, *args, **kwargs):
        form = RoleForm()
        return render(request, 'roles/role_create.html', {"form": form})


    
class RoleUpdateView(UpdateView):
    template_name = 'roles/role_create.html'
    login_url = '/login'
    form_class = RoleForm
    success_url = reverse_lazy('roles')
    model = Roles

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        self.object = self.model.objects.get(pk=pk)
        form = RoleForm(instance=self.object)
        return render(request, 'roles/role_create.html', {"form": form})       
    
    def form_valid(self, form):
        form.instance.user = self.request.user 
        form.save()
        return HttpResponseRedirect(self.get_success_url())
    

class RoleDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'roles/role_delete.html'
    success_url = reverse_lazy('roles')
    model = Roles
    login_url = '/login'


