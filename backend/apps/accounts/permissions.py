from rest_framework.permissions import BasePermission

def has_verified_identity(user):
    return bool(
        user
        and user.is_authenticated
        and user.is_active
        and (
            user.is_email_verified
            or user.is_phone_verified
        )
    )
    
class HasVerifiedIdentity(BasePermission):
    message = "A verified email or phone number is required."
    def has_permission(self, request, view):
        return has_verified_identity(request.user)