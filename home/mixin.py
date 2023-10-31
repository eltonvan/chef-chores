from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied


class CustomLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        '''  checks for object-level access control and 
        returns a 404 response if the current user does 
        not match the object's owner'''
        print("request.user.id", request.customuser.id)
        print("self.get_object().user.id", self.get_object().user.id)
        if self.get_object().user.id != request.user.id:
            template_name = 'home'
            return render(request, template_name, status=404)
        return super().dispatch(request, *args, **kwargs)
    



class CustomAuthorizationMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        ''' checks whether the user is authenticated 
        and handles the situation where the user 
        is not authenticated
        '''
        print("kwargs", kwargs)
        if kwargs.get("pk") is not None:

            if request.user.id != kwargs["pk"]:
                return redirect('authorized')
        return super().dispatch(request, *args, **kwargs)
    
class AdminRequiredMixin(UserPassesTestMixin):
    ''' checks whether the user is admin'''
    login_url = reverse_lazy('login')
    authorized_url = reverse_lazy('authorized')

    def test_func(self):
        return self.request.user.is_superuser
    

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        else:
            return redirect(self.authorized_url)