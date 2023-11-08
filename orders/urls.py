from django.urls import path
from . import views


urlpatterns = [
    path("restaurant", views.RestaurantListView.as_view(), name="restaurant_list"),
    path(
        "restaurant/create",
        views.RestaurantCreateView.as_view(),
        name="restaurant_create",
    ),
    path(
        "restaurant/<int:pk>",
        views.RestaurantDetailView.as_view(),
        name="restaurant_detail",
    ),
    path(
        "restaurant/<int:pk>/update",
        views.RestaurantUpdateView.as_view(),
        name="restaurant_update",
    ),
    path(
        "restaurant/<int:pk>/delete",
        views.RestaurantDeleteView.as_view(),
        name="restaurant_delete",
    ),
    path("location/", views.LocationListView.as_view(), name="location_list"),
    path(
        "location/create/", views.LocationCreateView.as_view(), name="location_create"
    ),
    path(
        "location/<int:pk>", views.LocationDetailView.as_view(), name="location_detail"
    ),
    path(
        "location/<int:pk>/update",
        views.LocationUpdateView.as_view(),
        name="location_update",
    ),
    path(
        "location/<int:pk>/delete",
        views.LocationDeleteView.as_view(),
        name="location_delete",
    ),
]
