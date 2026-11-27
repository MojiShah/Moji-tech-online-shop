from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

class RegisterAPITest(TestCase):
    
    def setUp(self):
        cache.clear()
        self.client = APIClient()
        self.url = reverse("accounts:register")
        self.data = {
            "email": "NEW@Example.com",
            "password": "Random!Test82#",
            "password_confirm": "Random!Test82#",
            "first_name": "Ali",
            "last_name": "Ahmadi",
        }
        
    def tearDown(self):
        cache.clear()
        
    def test_successful_registration(self):
        response = self.client.post(self.url,self.data,format="json",)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        user = User.objects.get(email="new@example.com")
        self.assertTrue(user.check_password(self.data["password"]))
        self.assertFalse(user.is_email_verified)
        self.assertNotIn("password",response.data,)
        self.assertNotIn("access",response.data,)
        
    def test_password_mismatch(self):
        self.data["password_confirm"] = "Different"
        response = self.client.post(self.url,self.data,format="json",)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(email="new@example.com").exists())
        
    def test_weak_password(self):
        self.data["password"] = "123"
        self.data["password_confirm"] = "123"
        response = self.client.post(self.url,self.data,format="json")
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_duplicate_email(self):
        self.client.post(self.url,self.data,format="json")
        self.data["email"] = "new@example.com"
        response = self.client.post(self.url,self.data,format="json")
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.filter(email="new@example.com").count(),1)

    def test_privilege_escalation_is_prevented(self):
        self.data["is_staff"] = True
        self.data["is_superuser"] = True
        self.data["is_email_verified"] = True
        response = self.client.post(self.url,self.data,format="json")
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        user = User.objects.get(email="new@example.com")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_email_verified)
        
    def test_invalid_email(self):
        self.data["email"] = "invalid-email"
        response = self.client.post(self.url,self.data,format="json")
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
