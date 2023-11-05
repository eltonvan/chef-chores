from django.test import TestCase
from django.urls import reverse
from .models import Location, Restaurant
from home.models import CustomUser as User
from django.test import Client


class LocationModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser"
        )  # Create a user using CustomUser
        self.user.set_password("testpassword")  # Set the password for the use
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant", user=self.user
        )
        self.location = Location.objects.create(
            name="Test Location",
            street="123 Test St",
            house_number="42",
            city="Test City",
            zip_code="12345",
            country="Test Country",
            phone_number="555-1234",
            email="test@example.com",
            opening_hours="Mon-Sat: 9am-6pm",
            restaurant_id=self.restaurant,
        )

    def test_location_model_str(self):
        self.assertEqual(str(self.location), "Test Location")

    def test_location_get_absolute_url(self):
        url = reverse("location_detail", kwargs={"pk": self.location.pk})
        self.assertEqual(self.location.get_absolute_url(), url)


class RestaurantModelTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            street="456 Test St",
            house_number="1",
            city="Test City",
            zip_code="54321",
            country="Test Country",
            phone_number="555-5678",
            email="test@example.com",
            website="https://www.testrestaurant.com",
            user=User.objects.create(username="test_user"),
        )

    def test_restaurant_model_str(self):
        self.assertEqual(str(self.restaurant), "Test Restaurant")

    def test_restaurant_get_absolute_url(self):
        url = reverse("restaurant_detail", kwargs={"pk": self.restaurant.pk})
        self.assertEqual(self.restaurant.get_absolute_url(), url)


class RestaurantViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client = Client()

    def test_restaurant_list_view(self):
        response = self.client.get(reverse("restaurant_list"))
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains the restaurant from the database.
        self.assertTemplateUsed(response, "restaurants/restaurant_list.html")
        # check that the user is not logged in
        self.assertFalse(response.context["user"].is_authenticated)
        # check that the user is logged in
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("restaurant_list"))
        self.assertTrue(response.context["user"].is_authenticated)
        #check that only the logged in user can see the restaurant

        


    def test_restaurant_detail_view(self):
        restaurant = Restaurant.objects.create(name="Test Restaurant", user=self.user)
        response = self.client.get(
            reverse("restaurant_detail", kwargs={"pk": restaurant.pk})
        )
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the rendered context contains the restaurant from the database.
        self.assertContains(response, "Test Restaurant")
        # check that only the logged in user can see the restaurant
        self.assertFalse(response.context["user"].is_authenticated)


    def test_restaurant_create_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("restaurant_create"))
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
    
        # that right user is saved in the form
        self.assertEqual(response.context["form"].instance.user, self.user)
        # check the form is valid
        self.assertTrue(response.context["form"].is_valid())
        # check that the form is rendered correctly
        self.assertContains(response, "form")
        # check the user is redirected to page after form submission
        response = self.client.post(
            reverse("restaurant_create"),
            {
                "name": "Test Restaurant",
                "street": "123 Test St",
                "house_number": "42",
                "city": "Test City",
                "zip_code": "12345",
                "country": "Test Country",
                "phone_number": "555-1234",
                "email": "testﬂ@example.com",
                "website": "https://www.testrestaurant.com",
                "user": self.user,
            },)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/restaurant/1")


    def test_restaurant_update_view(self):
        self.client.login(username="testuser", password="testpassword")
        restaurant = Restaurant.objects.create(name="Test Restaurant", user=self.user)
        response = self.client.get(
            reverse("restaurant_update", kwargs={"pk": restaurant.pk})
        )
        self.assertEqual(response.status_code, 200)
