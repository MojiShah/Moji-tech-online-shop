from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

import logging

from django.db import connection,DatabaseError

from drf_spectacular.utils import extend_schema

from .serializers import (
    HealthCheckSerializer,
    DatabaseHealthSerializer
)

logger = logging.getLogger(__name__)

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
    
class DatabaseHealthAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    
    @extend_schema(
        tags=["Core"],
        summary="Check database Health",
        description="Checks connectivity to PostgreSQL.",
        responses={
            200: DatabaseHealthSerializer,
            503: DatabaseHealthSerializer,
        },
    )
    
    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            data = {
            "status": "ok",
            "service": "database",
            }
            response_status = status.HTTP_200_OK
        except DatabaseError:
            logger.warning("Database health check failed",exc_info=True)
            data = {
                "status": "unavailable",
                "service": "database",
            }
            response_status = (status.HTTP_503_SERVICE_UNAVAILABLE)

        serializer = DatabaseHealthSerializer(data)
        return Response(serializer.data,status=response_status)

