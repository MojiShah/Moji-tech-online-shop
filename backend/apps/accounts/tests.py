from django.test import TestCase
from django.contrib.auth import(
    get_user_model,
    authenticate,
)
from django.core.exceptions import ValidationError
from django.db import (
    IntegrityError,
    transaction,
)

User = get_user_model()
# Create your tests here.
class UserModelTest(TestCase):
    def test_create_user_with_email(self):
        user = User.objects.create_user(
            email="ALI@Example.com",
            password="TestPassword123!",
        )
        self.assertEqual(user.email,"ali@example.com",)
        self.assertTrue(user.check_password("TestPassword123!"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_email_verified)
        
    def test_create_phone_only_users(self):
        first_user = User.objects.create_user(phone_number="09121234567",)
        second_user = User.objects.create_user(phone_number="09121234568",)
        self.assertEqual(first_user.phone_number,"+989121234567",)
        self.assertIsNone(first_user.email)
        self.assertIsNone(second_user.email)
        self.assertFalse(first_user.has_usable_password())
        self.assertFalse(first_user.is_phone_verified)
        
    def test_user_requires_identifier(self):
        with self.assertRaises(ValueError):
            User.objects.create_user()
            
    def test_invalid_phone_number(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user(phone_number="12345",)
            
    def test_duplicate_email_database_constraint(self):
        User.objects.create_user(email="customer@example.com",password="TestPassword123!",) 
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                User.objects.create(email="CUSTOMER@example.com",password="!",)
                
    def test_missing_identifier_database_constraint(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                User.objects.create(email=None,phone_number=None,password="!",)
                
    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email="admin@example.com",
            password="AdminPassword123!",
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
        
    def test_email_authentication(self):
        user = User.objects.create_user(
            email="admin@example.com",
            password="TestPassword123!",
        )

        authenticated_user = authenticate(
            username="ADMIN@EXAMPLE.COM",
            password="TestPassword123!",
        )
        self.assertEqual(authenticated_user,user,)

    def test_verified_email_requires_email(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                User.objects.create(
                    phone_number="+989121234567",
                    is_email_verified=True,
                    password="!",
                )