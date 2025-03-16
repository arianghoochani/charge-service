from rest_framework import serializers
from django.core.validators import RegexValidator
from .classes import ChargingRequestValidatorInput, CheckAuthorityRequest,InsertACLRequest
from .validators import validate_UUID, validate_token, validate_URL, validate_legalString
from .models import ChargingRequestLog


class ChargingRequestValidatorInputSerializer(serializers.Serializer):
    station_id = serializers.CharField(max_length=36, min_length=36, validators=[validate_UUID])
    driver_token = serializers.CharField(max_length=80, min_length=20, validators=[validate_token])
    callback_url = serializers.CharField(validators=[validate_URL])

    def create(self, validated_data):
        return ChargingRequestValidatorInput(**validated_data)

class ChargingRequestValidatorResponseSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=50, min_length=1, validators=[validate_legalString])
    message = serializers.CharField(max_length=300, min_length=1, validators=[validate_legalString])

class CheckAuthorityRequestSerializer(serializers.Serializer):
    station_id = serializers.CharField(max_length=36, min_length=36, validators=[validate_UUID])
    driver_token = serializers.CharField(max_length=80, min_length=20, validators=[validate_token])
    callback_url = serializers.CharField(validators=[validate_URL])
    request_time = serializers.DateTimeField()  

    def create(self, validated_data):
        return CheckAuthorityRequest(**validated_data)

class CheckAuthorityResponseSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=300, min_length=1, validators=[validate_legalString])

class ChargingRequestLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargingRequestLog
        fields = '__all__'  # Include all fields
        
class InsertACLRequestSerializer(serializers.Serializer):
    station_id = serializers.CharField(max_length=36, min_length=36, validators=[validate_UUID])
    driver_token = serializers.CharField(max_length=80, min_length=20, validators=[validate_token])
    def create(self, validated_data):
        return InsertACLRequest(**validated_data)

class InsertACLResponseSerializer(serializers.Serializer):
    flag = serializers.CharField(max_length=300, min_length=1, validators=[validate_legalString])
