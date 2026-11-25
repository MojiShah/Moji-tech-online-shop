from django.test import SimpleTestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from unittest.mock import patch
from django.db import OperationalError

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
        
class DatabaseHealthAPITest(SimpleTestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("core:database-health")
        
    @patch("apps.core.views.connection")
    def test_database_is_available(self, mock_connection):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.json(),
            {
                "status":"ok",
                "service":"database"
            }
        )
        mock_cursor = (mock_connection.cursor.return_value.__enter__.return_value)
        mock_cursor.execute.assert_called_once_with("SELECT 1")

    @patch("apps.core.views.connection")
    def test_database_is_unavailable(self, mock_connection):
        mock_connection.cursor.side_effect = (OperationalError("Connection failed"))
        with self.assertLogs("apps.core.views",level="WARNING"):
            response = self.client.get(self.url)
            
        self.assertEqual(response.status_code,status.HTTP_503_SERVICE_UNAVAILABLE,)
        self.assertEqual(response.json(),
            {
                "status": "unavailable",
                "service": "database",
            }
        )
