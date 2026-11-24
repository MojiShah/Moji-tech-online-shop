from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from drf_spectacular.utils import extend_schema

from .serializers import HealthCheckSerializer

# Create your views here.
class HealthCheckAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    
    @extend_schema(
        tags=["core"],
        summary="Check API health",
        description="Checks whether the API service is running.",
        responses={200: HealthCheckSerializer},
    )
    
    def get(self,request):
        data = {
            "status": "ok",
            "service": "Online Tech API",
            "version": "1.0.0",
        }
        
        serializer = HealthCheckSerializer(data)
        return Response(serializer.data,status=status.HTTP_200_OK)
