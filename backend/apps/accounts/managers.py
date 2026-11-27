from django.contrib.auth.models import BaseUserManager
from .validators import (
    normalize_email_address,
    normalize_phone_number,
    )

class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_user(self,email=None,password=None,phone_number=None,**extra_fields):
        email = normalize_email_address(email)
        phone_number = normalize_phone_number(phone_number)
        
        if not email and not phone_number:
            raise ValueError("Email or phone number is required.")
        
        if not phone_number and not password:
            raise ValueError("Email-only accounts require a password.")
        
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        
        user = self.model(email=email,phone_number=phone_number,**extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
            
        user.full_clean()
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None,**extra_fields):
        
        if not normalize_email_address(email):
            raise ValueError("Superuser must have an email.")
        
        if not password:
            raise ValueError("Superuser must have a password.")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")
        
        return self.create_user(email=email,password=password,**extra_fields)
    
    def get_by_natural_key(self,username):
        email = normalize_email_address(username)
        if not email:
            raise self.model.DoesNotExist
        return self.get(email__iexact=email)