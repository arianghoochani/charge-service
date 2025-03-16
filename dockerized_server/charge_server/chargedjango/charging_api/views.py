from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.serializers import ValidationError
from django.utils.timezone import now 
from .serializers import ChargingRequestValidatorInputSerializer, ChargingRequestValidatorResponseSerializer,ChargingRequestLogSerializer
from .classes import ChargingRequestValidatorResponse
from .models import ChargingRequestLog
from confluent_kafka import Producer
import json

KAFKA_BROKER = "kafka:9092"
TOPIC_NAME = "charging_requests"

producer_conf = {'bootstrap.servers': KAFKA_BROKER}
producer = Producer(producer_conf)

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
        message = {
            "station_id": serializer.validated_data["station_id"],
            "driver_token": serializer.validated_data["driver_token"],
            "callback_url": serializer.validated_data["callback_url"]
        }
        producer.produce(TOPIC_NAME, json.dumps(message))
        producer.flush()
    except ValidationError :
        status_code = "0"
        attributeName = list(serializer.errors.keys())[0]
        status = attributeName
    except:
        status = "unknown"

    chargingRequestValidatorResponse = ChargingRequestValidatorResponse(status = status)
    serializer = ChargingRequestValidatorResponseSerializer(chargingRequestValidatorResponse)
    return Response(serializer.data)

@api_view(['GET'])
def getRequestLog(request):
    logs = ChargingRequestLog.objects.all()

    # Serialize the queryset
    serializer = ChargingRequestLogSerializer(logs, many=True)

    # Return the JSON response
    return Response(serializer.data)


@api_view(['POST'])
def addACL(request):
    ACL = [
        ("550e8400-e29b-41d4-a716-446655440000","user-123~valid.token")
    ]
    station_id = request.data.get("station_id")
    driver_token = request.data.get("driver_token")
    request_time = request.data.get("request_time")
    decision = "allowed" if (station_id, driver_token) in ACL else "not_allowed"

    # Log the request
    try:
        # Fetch the most recent record that matches the given station_id and driver_token
        log_entry = ChargingRequestLog.objects.filter(
            station_id=station_id,
            driver_token=driver_token
        ).latest('request_time')  # Get the latest request based on time

        # Update the decision and decision_time
        log_entry.decision = decision
        log_entry.decision_time = now()
        log_entry.save(force_update=True)

        return Response({"status": decision, "message": "Decision updated successfully"})

    except ChargingRequestLog.DoesNotExist:
        return Response({"status": "error", "message": "No matching record found"}, status=404)
    
