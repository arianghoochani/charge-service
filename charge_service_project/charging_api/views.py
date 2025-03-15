from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.serializers import ValidationError
from django.utils.timezone import now 
from .serializers import ChargingRequestValidatorInputSerializer, ChargingRequestValidatorResponseSerializer
from .classes import ChargingRequestValidatorResponse
from .models import ChargingRequestLog

@api_view(['POST'])
def chargingRequestValidator(request):
    status = "unknown"
    try:
        serializer = ChargingRequestValidatorInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status = "accepted"
        chargingRequestLog = ChargingRequestLog(
                station_id=serializer.validated_data["station_id"],
                driver_token=serializer.validated_data["driver_token"],
                callback_url=serializer.validated_data["callback_url"],
                request_time=now(),
                decision_time=None,
                decision="unknown"
            )
        chargingRequestLog.save(force_insert=True)
    except ValidationError :
        status_code = "0"
        attributeName = list(serializer.errors.keys())[0]
        status = attributeName
    except:
        status = "unknown"

    chargingRequestValidatorResponse = ChargingRequestValidatorResponse(status = status)
    serializer = ChargingRequestValidatorResponseSerializer(chargingRequestValidatorResponse)
    return Response(serializer.data)