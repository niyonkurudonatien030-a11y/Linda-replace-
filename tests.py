from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Post

class NetworkApiTests(APITestCase):
    def test_registration_creates_user_and_token(self):
        response = self.client.post(reverse("register"), {
            "username": "sampleuser", "email": "sample@example.com",
            "password": "A-strong-test-password-42"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertTrue(User.objects.filter(username="sampleuser").exists())

    def test_authenticated_user_can_publish_post(self):
        user = User.objects.create_user(username="writer", email="writer@example.com", password="A-strong-test-password-42")
        self.client.force_authenticate(user=user)
        response = self.client.post("/api/posts/", {"body": "A first professional update."}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

    def test_anonymous_user_cannot_publish_post(self):
        response = self.client.post("/api/posts/", {"body": "Anonymous spam"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
