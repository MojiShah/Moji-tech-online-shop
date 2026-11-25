from django.test import SimpleTestCase
from django.urls import reverse
from django.test import override_settings


from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.exceptions import ValidationError

from unittest.mock import patch
from django.db import OperationalError

from .exceptions import custom_exception_handler

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
        
class ExceptionHandlerTest(SimpleTestCase):

    def setUp(self):
        self.client = APIClient()

    def test_validation_error_format(self):
        exc = ValidationError({"email": ["Invalid email."]})
        response = custom_exception_handler(exc,context={},)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,)
        self.assertEqual(
            response.data,
            {
                "error": {
                    "status_code": 400,
                    "details": {
                        "email": ["Invalid email."]
                    },
                }
            },
        )

    def test_method_not_allowed_format(self):
        url = reverse("core:health-check")
        response = self.client.post(url,{},format="json",)
        self.assertEqual(response.status_code,status.HTTP_405_METHOD_NOT_ALLOWED,)
        data = response.json()
        self.assertEqual(data["error"]["status_code"],405,)
        self.assertIn("detail",data["error"]["details"],)
        self.assertIn("GET",response["Allow"],)
        
@override_settings(CORS_ALLOWED_ORIGINS=["http://localhost:3000"],CORS_ALLOW_ALL_ORIGINS=False)
class CorsTest(SimpleTestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("core:health-check")
        
    def test_allowed_origin(self):
        response = self.client.options(
            self.url,
            HTTP_ORIGIN="http://localhost:3000",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="GET",
        )
        self.assertEqual(
            response["Access-Control-Allow-Origin"],
            "http://localhost:3000",
        )
        
    def test_disallowed_origin(self):
        response = self.client.options(
            self.url,
            HTTP_ORIGIN="https://unknown-site.example",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="GET",
        )
        self.assertFalse(response.has_header("Access-Control-Allow-Origin"))
