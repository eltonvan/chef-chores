from django.test import TestCase
from django.urls import reverse, reverse_lazy
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
        self.user2 = User.objects.create_user(
            username="testuser2", password="testpassword2", email="test@gamil.com"
        )
        self.client = Client()
        self.client.login(username="testuser", password="testpassword")
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
            user=self.user,
        )

    def test_restaurant_list_view(self):
        response = self.client.get(reverse("restaurant_list"))
        # Check that the response is 200 OK.
        self.client.login(username="testuser", password="testpassword")
        self.assertEqual(response.status_code, 200)
        # self.client.logout()

        # Check that the rendered context contains the restaurant from the database.
        self.assertTemplateUsed(response, "restaurants/restaurant_list.html")
        # check that the user is not logged in
        # self.assertFalse(response.context["user"].is_authenticated)
        # check that the user is logged in
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("restaurant_list"))
        self.assertTrue(response.context["user"].is_authenticated)
        # check that only the logged in user can see the restaurant

    def test_restaurant_detail_view_other_user(self):
        # login a different user than the one that created the restaurant
        login = self.client.login(username="testuser2", password="testpassword2")

        response = self.client.get(
            reverse("restaurant_detail", kwargs={"pk": 1}), follow=True
        )

        # Check that the redirect url is correct
        self.assertRedirects(
            response, reverse("authorized"), status_code=302, target_status_code=200
        )

        # check that the page contains the text "not authorized"
        self.assertContains(response, "not authorized")

    def test_restaurant_detail_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("restaurant_detail", kwargs={"pk": self.restaurant.pk})
        )
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains the restaurant from the database.
        self.assertContains(response, self.restaurant.name)

    def test_restaurant_create_view(self):
        self.client.login(username="testuser", password="testpassword")
        self.user = User.objects.get(username="testuser")
        response = self.client.get(reverse("restaurant_create"))
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the form is rendered correctly
        self.assertContains(response, "form")

        # check the user is redirected to page after form submission
        response = self.client.post(
            reverse("restaurant_create"),
            {
                "name": "Test Restaurant1",
                "street": "123 Test St",
                "house_number": "42",
                "city": "Test City",
                "zip_code": "12345",
                "country": "Test Country",
                "phone_number": "555-1234",
                "email": "email3@example.com",
                "website": "https://www.testrestaurant.com",
                "user": self.user.id,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("restaurant_list"))
        expected_url = reverse_lazy("restaurant_list")
        self.assertEqual(response.url, expected_url)

        # Check if the user is correctly associated with the Restaurant in the database
        restaurant = Restaurant.objects.get(name="Test Restaurant1")
        self.assertEqual(restaurant.user, self.user)

    def test_restaurant_update_view(self):
        self.client.login(username="testuser", password="testpassword")
        restaurant = Restaurant.objects.create(
            name="Test Restaurant", user=self.user, email="test@gmail.com"
        )
        response = self.client.get(
            reverse("restaurant_update", kwargs={"pk": restaurant.pk})
        )
        self.assertEqual(response.status_code, 200)


class LocationViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", password="testpassword2", email="testing@gmail.com"
        )

        self.client = Client()

        self.client.login(username="testuser", password="testpassword")

        # create  test restaurants
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            street="456 Test St",
            house_number="1",
            city="Test City",
            zip_code="54321",
            country="Test Country",
            phone_number="555-5678",
            email="restaurant1@examplet.com",
            user=self.user,
        )

        self.restaurant2 = Restaurant.objects.create(
            name="Test Restaurant2",
            street="456 Test St",
            house_number="1",
            city="Test City",
            zip_code="54321",
            country="Test Country",
            phone_number="555-5678",
            email="restaurant2@examplet.com",
            user=self.user2,
        )

        # create test locations
        self.location = Location.objects.create(
            name="Test Location",
            street="123 Test St",
            house_number="42",
            city="Test City",
            zip_code="12345",
            country="Test Country",
            phone_number="555-1234",
            email="loacation@gmail.com",
            restaurant_id=self.restaurant,
        )

        self.location2 = Location.objects.create(
            name="Test Location2",
            street="123 Test St",
            house_number="42",
            city="Test City",
            zip_code="12345",
            country="Test Country",
            email="loacation2@gmail.com",
            restaurant_id=self.restaurant2,
        )

    def test_location_list_view(self):
        response = self.client.get(reverse("location_list"))
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains the location from the database.
        self.assertEqual(response.context["locations"][0].name, self.location.name)

    def test_location_detail_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("location_detail", kwargs={"pk": self.location.pk})
        )
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains the location from the database.
        self.assertContains(response, self.location.name)

    def test_location_detail_view_wrong_user(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("location_detail", kwargs={"pk": self.location2.pk}), follow=True
        )
        # Check that the redirect url is correct
        self.assertRedirects(
            response, reverse("authorized"), status_code=302, target_status_code=200
        )

        # check that the page contains the text "not authorized"
        self.assertContains(response, "not authorized")

    def test_location_create_view(self):
        self.client.login(username="testuser", password="testpassword")
        self.user = User.objects.get(username="testuser")
        self.restaurant = Restaurant.objects.get(name="Test Restaurant", user=self.user)
        response = self.client.get(reverse("location_create"))
        # Check that the response is 200.
        self.assertEqual(response.status_code, 200)

        # Check that the form is rendered correctly
        self.assertContains(response, "form")

        # check the user is redirected to page after form submission
        response = self.client.post(
            reverse("location_create"),
            {
                "name": "Test Location3",
                "street": "123 Test St",
                "house_number": "42",
                "city": "Test City",
                "zip_code": "12345",
                "country": "Test Country",
                "phone_number": "555-1234",
                "email": "email3@gmail.com",
                "opening_hours": "Mon-Sat: 9am-6pm",
                "restaurant_id": self.restaurant.id,
            },
        )
        print(response)

        expected_url = reverse_lazy("location_list")
        self.assertEqual(response.url, expected_url)

        # self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("location_list"))

        # check that the user is correctly associated with the location in the database
        print(Location.objects.first())
        # location = Location.objects.first()
        location = Location.objects.get(name="Test Location3")
        self.assertEqual(location.restaurant_id, self.restaurant)
