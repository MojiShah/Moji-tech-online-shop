from django.test import SimpleTestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

# Create your tests here.
class HealthCheckAPITest(SimpleTestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("core:health-check")
        
    def test_health_check_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_health_check_response_data(self):
        response = self.client.get(self.url)
        self.assertEqual(response.json(),
            {
                "status": "ok",
                "service": "Online Tech API",
                "version": "1.0.0",
            },
        )

    def test_post_method_is_not_allowed(self):
        response = self.client.post(self.url,{},format="json",)
        self.assertEqual(response.status_code,status.HTTP_405_METHOD_NOT_ALLOWED,)
