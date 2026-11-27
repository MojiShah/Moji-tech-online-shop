from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError,transaction

from rest_framework import serializers

from .validators import normalize_email_address

User = get_user_model()

class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "is_email_verified",
            "is_phone_verified",
        )
        
        read_only_fields = fields
        
class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254,)
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
        max_length=128,
        style={"input_type": "password"},
    )
    password_confirm = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
        max_length=128,
        style={"input_type": "password"},
    )
    first_name = serializers.CharField(max_length=150,required=False,allow_blank=True,)
    last_name = serializers.CharField(max_length=150,required=False,allow_blank=True,)
    
    def validate_email(self,value):
        email = normalize_email_address(value)
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("An account with this email already exists.")

        return email
    
    def validate(self, attrs):
        password = attrs["password"]
        password_confirm = attrs["password_confirm"]
        if password != password_confirm:
            raise serializers.ValidationError({
                "password_confirm": ["Passwords do not match."]
            })
            
        candidate_user = User(
            email = attrs["email"],
            first_name = attrs.get("first_name",""),
            last_name = attrs.get("last_name",""),
        )
        
        try:
            validate_password(password,user=candidate_user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError({"password":exc.messages}) from exc
        
        return attrs
    
    def create(self,validated_data):
        validated_data.pop("password_confirm")
        try:
            with transaction.atomic():
                user = User.objects.create_user(**validated_data)
        except DjangoValidationError as exc:
            details = getattr(exc,"message_dict",None) or exc.message
            raise serializers.ValidationError(details) from exc
        except IntegrityError as exc:
            email = validated_data["email"]
            if User.objects.filter(email__iexact=email).exists():
                raise serializers.ValidationError({
                    "email":["An account with this email already exists."]
                })
            raise
        return user
        