from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Project

class ProjectAPIViewTests(APITestCase):
    def setUp(self):
        self.url = '/api/projects/' 

        self.username = 'testuser'
        self.password = 'password123'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        
        self.project = Project.objects.create(name="Sample Project 1", key="SP1")

    def test_get_project_list_without_auth(self):
        response = self.client.get(self.url)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
