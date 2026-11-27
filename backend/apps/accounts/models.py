from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)

from django.core.exceptions import ValidationError
from django.utils import timezone

from .managers import UserManager
from .validators import (
    normalize_email_address,
    normalize_phone_number,
    )
# Create your models here.
class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True,null=True,blank=True,)
    phone_number = models.CharField(max_length=13,unique=True,null=True,blank=True,)
    first_name = models.CharField(max_length=150,blank=True,)
    last_name = models.CharField(max_length=150,blank=True,)
    is_email_verified = models.BooleanField(default=False,)
    is_phone_verified = models.BooleanField(default=False,)
    is_active = models.BooleanField(default=True,)
    is_staff = models.BooleanField(default=False,)
    date_joined = models.DateTimeField(default=timezone.now,)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name ="User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(email__isnull=False) | Q(phone_number__isnull=False)
                ),
                name="user_requires_email_or_phone",
            ),
            models.CheckConstraint(
                condition=(
                    Q(email__isnull=True) | ~Q(email="")
                ),
                name="user_email_not_empty"
            ),
            models.CheckConstraint(
                condition=(
                    Q(phone_number__isnull=True) | Q(phone_number__regex=( r"^\+989[0-9]{9}$"))
                ),
                name="user_phone_valid_format",
            ),
            models.UniqueConstraint(
                Lower("email"),
                name="user_email_case_insensitive_unique",
            ),
            models.CheckConstraint(
                condition=(
                    Q(is_email_verified=False) | Q(email__isnull=False)
                ),
                name="user_verified_email_required",
            ),
            models.CheckConstraint(
                condition=(
                    Q(is_phone_verified=False) | Q(phone_number__isnull=False)
                ),
                name="user_verified_phone_required",
            )
        ]
        
    def clean(self):
        super().clean()
        self.email = normalize_email_address(self.email)
        try:
            self.phone_number = normalize_phone_number(self.phone_number)
        except ValidationError as exc:
            raise ValidationError({"phone_number": exc.messages}) from exc
        
        if not self.email and not self.phone_number:
            raise ValidationError("Email or phone number is required.")

    def get_full_name(self):
        return (f"{self.first_name} {self.last_name}").strip()
    
    def get_short_name(self):
        return self.first_name or str(self)
    
    def __str__(self):
        return self.email or self.phone_number or str(self.pk)