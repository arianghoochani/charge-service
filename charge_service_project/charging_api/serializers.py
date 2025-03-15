from rest_framework import serializers
from django.core.validators import RegexValidator
from .classes import ChargingRequestValidator
from .validators import validate_UUID, validate_token, validate_URL


class ChargingRequestValidatorSerializer(serializers.Serializer):
    station_id = serializers.CharField(max_length=36, min_length=36, validators=[validate_UUID])
    driver_token = serializers.CharField(max_length=80, min_length=20, validators=[validate_driver_token])
    callback_url = serializers.CharField(validators=[validate_URL])

    def create(self, validated_data):
        return CheckAuthorityRequest(**validated_data)