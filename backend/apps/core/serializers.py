from rest_framework import serializers


class HealthCheckSerializer(serializers.Serializer):
    status = serializers.CharField()
    service = serializers.CharField()
    version = serializers.CharField()
    
class DatabaseHealthSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=["ok","unavailable"])
    service = serializers.CharField()
    
class ErrorDetailSerializer(serializers.Serializer):
    status_code = serializers.IntegerField()
    details = serializers.JSONField()

class APIErrorSerializer(serializers.Serializer):
    error = ErrorDetailSerializer()