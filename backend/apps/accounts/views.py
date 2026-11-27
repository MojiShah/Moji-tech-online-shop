from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle

from drf_spectacular.utils import extend_schema

from apps.core.serializers import APIErrorSerializer
from .serializers import (
    RegisterSerializer,
    UserPublicSerializer
)

# Create your views here.
class RegisterAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "register"

    @extend_schema(
         tags=["Authentication"],
         summary="Register with email and password",
         description=(
            "Creates a new account without issuing JWT tokens. "
            "Email verification is required before login."
        ),
         request=RegisterSerializer,
         responses={
            201: UserPublicSerializer,
            400: APIErrorSerializer,
            429: APIErrorSerializer,
        },
    )
    
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response_serializer = UserPublicSerializer(user)
        return Response(response_serializer.data,status=status.HTTP_201_CREATED)