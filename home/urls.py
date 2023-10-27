from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name = 'home'),
    path('authorized', views.AuthorizedView.as_view()),
    path('login',views.LoginInterfaceView.as_view(), name = 'login'),
    path('logout', views.LogoutInterfaceView.as_view(), name = 'logout'),
    path('signup', views.SignupView.as_view(), name = 'signup'),
    path('user/edit', views.UpdateView.as_view(), name = 'update'),

    path('roles', views.RoleListView.as_view(), name = 'roles'),
    path('roles/create', views.RoleCreateView.as_view(), name = 'role_create'),
    path('roles/<int:pk>', views.RoleDetailView.as_view(), name = 'role_detail'),
    path('roles/<int:pk>/edit', views.RoleUpdateView.as_view(), name = 'role_update'),
    path('roles/<int:pk>/delete', views.RoleDeleteView.as_view(), name = 'role_delete'),

    
    
    ]