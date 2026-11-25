from django.urls import path
from .views import (
    HealthCheckAPIView,
    DatabaseHealthAPIView
)

app_name = "core"

urlpatterns=[
    path( "health/",HealthCheckAPIView.as_view(),name="health-check",),
    path("health/db/",DatabaseHealthAPIView.as_view(),name="database-health",),
]