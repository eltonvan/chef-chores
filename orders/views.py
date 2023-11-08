from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from home.models import CustomUser, Roles
from .models import (
    Restaurant,
    Location,
)  # , Product, Count, Orders, PriceHistory, Product_supplier, ProdCategory, SupplierLocation, Supplier, OrderMethod


from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .forms import (
    RestaurantForm,
    LocationForm,
)  # , ProductForm, CountForm, OrdersForm, PriceHistoryForm, Product_supplierForm, ProdCategoryForm, SupplierLocationForm, SupplierForm, OrderMethodForm
from django.urls import reverse_lazy
from home.mixin import (
    CustomLoginRequiredMixin,
    CustomAuthorizationMixin,
    AdminRequiredMixin,
)
from django.http import HttpResponseRedirect


class RestaurantListView(CustomAuthorizationMixin, ListView):
    model = Restaurant
    template_name = "restaurants/restaurant_list.html"
    context_object_name = "restaurants"
    ordering = ["name"]
    paginate_by = 10


class RestaurantDetailView(CustomAuthorizationMixin, DetailView):
    model = Restaurant
    template_name = "restaurants/restaurant_detail.html"
    context_object_name = "restaurant"
    login_url = "login"


class RestaurantCreateView(LoginRequiredMixin, CreateView):
    model = Restaurant
    template_name = "restaurants/restaurant_create.html"

    success_url = reverse_lazy("restaurant_list")

    fields = [
        "name",
        "street",
        "city",
        "house_number",
        "zip_code",
        "country",
        "phone_number",
        "email",
        "website",
    ]

    def get(self, request, *args, **kwargs):
        form = RestaurantForm(user=request.user.pk)
        return render(request, "restaurants/restaurant_create.html", {"form": form})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class RestaurantUpdateView(UpdateView):
    model = Restaurant
    template_name = "restaurants/restaurant_update.html"
    form_class = RestaurantForm
    success_url = reverse_lazy("restaurant_list")

    # def get(self, request, *args, **kwargs):
    #     pk = self.kwargs.get("pk")
    #     self.object = self.model.objects.get(pk=pk)
    #     form = RestaurantForm(instance=self.object)
    #     return render(request, "restaurants/restaurant_update.html", {"form": form})

    def get(self, request, *args, **kwargs):
        form = RestaurantForm(user=request.user.pk)
        return render(request, "restaurants/restaurant_update.html", {"form": form})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class RestaurantDeleteView(CustomLoginRequiredMixin, DeleteView):
    model = Restaurant
    template_name = "restaurants/restaurant_delete.html"
    success_url = reverse_lazy("restaurant_list")


class LocationListView(CustomAuthorizationMixin, ListView):
    model = Location
    template_name = "location/location_list.html"
    context_object_name = "locations"
    ordering = ["name"]
    paginate_by = 10


class LocationDetailView(CustomAuthorizationMixin, DetailView):
    model = Location
    template_name = "location/location_detail.html"
    context_object_name = "location"
    login_url = "login"


class LocationCreateView(LoginRequiredMixin, CreateView):
    model = Location
    template_name = "location/location_create.html"
    form_class = LocationForm
    success_url = reverse_lazy("location_list")

    def get(self, request, *args, **kwargs):
        # Assign the logged-in user to the form
        form = LocationForm(user=request.user.pk)
        return render(request, "location/location_create.html", {"form": form})

    def form_valid(self, form):
        # save the logged-in user to the form
        form.instance.user = self.request.user
        return super().form_valid(form)


class LocationUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = Location
    template_name = "location/location_update.html"
    form_class = LocationForm
    success_url = reverse_lazy("locations")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = RestaurantForm(instance=self.object, user=request.user)
        return render(request, "location/location_update.html", {"form": form})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return HttpResponseRedirect(self.get_success_url())


class LocationDeleteView(CustomLoginRequiredMixin, DeleteView):
    model = Location
    template_name = "location/location_delete.html"
    success_url = reverse_lazy("locations")
