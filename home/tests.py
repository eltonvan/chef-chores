from django.test import TestCase
from django.urls import reverse
from .models import CustomUser, Roles
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, RoleForm


class UserTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = CustomUser.objects.create_user(
            is_superuser=True,
            username="testuser1",
            password="abc123",
            email="user1@testsite.com",
            first_name="Test",
            last_name="User",
            phone_number="1234567890",
            city="Test City",
            zip_code="12345",
            country="Test Country",
            is_staff=True,
        )
        testuser1.save()

        testuser2 = CustomUser.objects.create_user(
            username="testuser2",
            password="abc123",
            email="user2@testsite.com",
            first_name="Test",
            last_name="User",
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
        self.client.login(username="testuser1", password="abc123")
        response = self.client.get(reverse("user_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser1")
        self.assertTemplateUsed(response, "home/user_list.html")


class RolesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        name = "Test Role"
        description = "Test Description"
        role = Roles.objects.create(name=name, description=description)

    def test_roles_content(self):
        role = Roles.objects.get(id=1)
        expected_object_name = f"{role.name}"
        # Check that the role has the correct name and description
        self.assertEquals(expected_object_name, "Test Role")
        self.assertEquals(role.description, "Test Description")

    def test_roles_list_view(self):
        # Create a test user and log them in
        test_user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")
        test_user.roles.add(Roles.objects.get(name="Test Role"))

        response = self.client.get(reverse("roles"))
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the rendered context contains 1 role.
        self.assertContains(response, "Test Role")
        # Check that the rendered context contains the role from the database.
        self.assertTemplateUsed(response, "roles/role_list.html")


class UserRoleTests(TestCase):
    def setUp(self):
        role1 = Roles.objects.create(name="Role 1")
        role2 = Roles.objects.create(name="Role 2")

        # Create test users with unique email addresses
        self.user1 = CustomUser.objects.create_user(
            username="user1", password="password1", email="user1@example.com"
        )
        self.user2 = CustomUser.objects.create_user(
            username="user2", password="password2", email="user2@example.com"
        )
        # Add roles to the users
        self.user1.roles.add(Roles.objects.get(name="Role 1"))
        self.user2.roles.add(Roles.objects.get(name="Role 2"))

    def test_associate_roles_with_user(self):
        # Check that the users have the correct roles
        self.assertEqual(self.user1.roles.count(), 1)
        self.assertEqual(self.user2.roles.count(), 1)

    # broken!
    def test_retrieve_users_by_role(self):
        # Query users with Role 1
        users_with_role1 = Roles.objects.filter(name="Role 1")
        self.assertEqual(users_with_role1.count(), 1)
        self.assertEqual(users_with_role1[0], self.user1.roles.last())

        # Query users with Role 2
        users_with_role2 = Roles.objects.filter(name="Role 2")
        self.assertEqual(users_with_role2.count(), 1)
        self.assertEqual(users_with_role2[0], self.user2.roles.last())


class RoleListViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Create some roles associated with the user
        self.role1 = Roles.objects.create(name="Role 1")
        self.role2 = Roles.objects.create(name="Role 2")
        self.role3 = Roles.objects.create(name="Role 3")
        self.user.roles.add(self.role1, self.role2)

    def test_role_list_view_authenticated_user(self):
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Access the RoleListView
        response = self.client.get(reverse("roles"))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the user's associated roles are displayed in the template
        self.assertContains(response, "Role 1")
        self.assertContains(response, "Role 2")

        # Check if roles not associated with the user are not displayed
        self.assertNotContains(response, "Role 3")

    def test_role_list_view_unauthenticated_user(self):
        # Access the RoleListView without logging in
        response = self.client.get(reverse("roles"))

        # Check if the response status code is 302 (redirect to login)
        self.assertEqual(response.status_code, 302)

        # Check if the user is redirected to the login page
        self.assertRedirects(response, "/login?next=/roles")
