from rest_framework import status
from rest_framework.test import APITestCase
from users.models import CustomUser as User

from .models import Project


class ProjectAPIViewTests(APITestCase):
    def setUp(self):
        self.url = "/api/projects/"

        self.email = "testuser"
        self.password = "password123"
        self.user = User.objects.create_user(email=self.email, password=self.password)

        self.project = Project.objects.create(name="Sample Project 1", key="SP1")

    def test_get_project_list_authenticated(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
