from django.test import TestCase
from django.urls import reverse
from .models import CustomUser, Roles
from .forms import CustomUserCreationForm, RoleForm


class UserTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = CustomUser.objects.create_user(
            username="testuser1", password="abc123", 
            email="user1@testsite.com",
            first_name="Test", last_name="User",
            phone_number="1234567890",
            city="Test City",
            zip_code="12345",
            country="Test Country",
            is_staff=True, )
        testuser1.save()

        testuser2 = CustomUser.objects.create_user(
            username="testuser2", password="abc123",
            email="user2@testsite.com",
            first_name="Test", last_name="User",
            phone_number="1234567890", 
            city="Test City",   
            zip_code="12345",
            country="Test Country",
            is_staff=True, 
        )
        testuser2.save()

    def test_users_content(self):
        user = CustomUser.objects.get(id=1)
        expected_object_name = f"{user.username}"
        self.assertEquals(expected_object_name, "testuser1")
        self.assertEquals(user.email, "user1@testsite.com")
        self.assertEquals(user.first_name, "Test")
        self.assertEquals(user.last_name, "User")
        self.assertEquals(user.phone_number, "1234567890")
        self.assertEquals(user.city, "Test City")
        self.assertEquals(user.zip_code, "12345")
        self.assertEquals(user.country, "Test Country")
        self.assertEquals(user.is_staff, True)

    def test_users_list_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        #self.assertContains(response, "testuser1")
        self.assertTemplateUsed(response, "home/welcome.html")

class RolesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        name  = "Test Role"
        description = "Test Description"
        role = Roles.objects.create(name=name, description=description)

    def test_roles_content(self):
        role = Roles.objects.get(id=1)
        expected_object_name = f"{role.name}"
        self.assertEquals(expected_object_name, "Test Role")
        self.assertEquals(role.description, "Test Description")

    def test_roles_list_view(self):
        response = self.client.get(reverse("roles"))
        self.assertEqual(response.status_code, 302)
        self.assertContains(response, "Test Role")
        self.assertTemplateUsed(response, "roles/role_list.html")
