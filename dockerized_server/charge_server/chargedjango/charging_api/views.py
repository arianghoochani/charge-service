from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.serializers import ValidationError
from django.db import IntegrityError
from django.utils.timezone import now 
from .serializers import ChargingRequestValidatorInputSerializer, ChargingRequestValidatorResponseSerializer,ChargingRequestLogSerializer, CheckAuthorityRequestSerializer,CheckAuthorityResponseSerializer,InsertACLRequestSerializer,InsertACLResponseSerializer
from .classes import ChargingRequestValidatorResponse,CheckAuthorityResponse, CheckAuthorityRequest,InsertACLResponse
from .models import ChargingRequestLog, AccessControlList
from confluent_kafka import Producer
import json
from datetime import datetime, timedelta
import requests


KAFKA_BROKER = "kafka:9092"
TOPIC_NAME = "charging_requests"

producer_conf = {'bootstrap.servers': KAFKA_BROKER}
producer = Producer(producer_conf)

@api_view(['POST'])
def chargingRequestValidator(request):
    status = "unknown"
    # try:
    serializer = ChargingRequestValidatorInputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    status = "accepted"
    # chargingRequestLog = ChargingRequestLog(
    #         station_id=serializer.validated_data["station_id"],
    #         driver_token=serializer.validated_data["driver_token"],
    #         callback_url=serializer.validated_data["callback_url"],
    #         request_time=now(),
    #         decision_time=None,
    #         decision="unknown"
    #     )
    # chargingRequestLog.save(force_insert=True)
    message = {
        "station_id": serializer.validated_data["station_id"],
        "driver_token": serializer.validated_data["driver_token"],
        "callback_url": serializer.validated_data["callback_url"],
        "request_time": now().isoformat(),
    }
    producer.produce(TOPIC_NAME, json.dumps(message))
    producer.flush()
    # except ValidationError :
    #     attributeName = list(serializer.errors.keys())[0]
    #     status = attributeName
    # except:
    #     status = "unknown"

    chargingRequestValidatorResponse = ChargingRequestValidatorResponse(status = status)
    serializer = ChargingRequestValidatorResponseSerializer(chargingRequestValidatorResponse)
    return Response(serializer.data)

@api_view(['POST'])
def checkAuthority(request):
    decision = ""
    message = ""
    decisionTime = now()
    checkAuthorityRequest = CheckAuthorityRequest()
    try:
        serializer = CheckAuthorityRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        checkAuthorityRequest = serializer.save()
        request_time = datetime.fromisoformat(checkAuthorityRequest.replace("Z", "+00:00"))
        decision_time = datetime.fromisoformat(now().replace("Z", "+00:00"))
        time_difference = decision_time - request_time
        if time_difference <= timedelta(minutes=2):
            ACl_id = checkAuthorityRequest.station_id + checkAuthorityRequest.driver_token
            if AccessControlList.objects.filter(ACL_id=ACL_id).exists():
                decision = "allowed"
                message = "Access granted"
            else:
                decision = "not_allowed"
                message = "Access denied"
        else:
            decision = "unknown"
            message = "Request is too old"
        chargingRequestLog = ChargingRequestLog(
        station_id=checkAuthorityRequest.station_id,
        driver_token= checkAuthorityRequest.driver_token,
        callback_url=checkAuthorityRequest.callback_url,
        request_time=checkAuthorityRequest.request_time,
        decision_time=decision_time,
        decision=decision
    )
        chargingRequestLog.save(force_insert=True)
    except:
        message = "An error occurred while proccessing charging request."
    if checkAuthorityRequest.callback_url:
        callbackresponse = requests.post(checkAuthorityRequest.callback_url, json={"message": message})
    checkAuthorityResponse = CheckAuthorityResponse(message = message)
    serializer = CheckAuthorityResponseSerializer(checkAuthorityResponse)

    return Response(serializer.data)
    
 

@api_view(['POST'])
def insertACL(request):
    data = request.data
    # try:
    serializer = InsertACLRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    insertACLRequest = serializer.save()
    acl_id = insertACLRequest.station_id + insertACLRequest.driver_token

    if not AccessControlList.objects.filter(ACL_id=acl_id).exists():
        
        acl_entry = AccessControlList(
            ACL_id=acl_id,
            station_id=insertACLRequest.station_id,
            driver_token=insertACLRequest.driver_token,
        )
        acl_entry.save(force_insert=True)
        flag = "success"
    else:
        flag = "exists"
    # except:
    #     flag = "error"
    insertACLResponse = InsertACLResponse(flag = flag)
    serializer = InsertACLResponseSerializer(insertACLResponse)    
    return Response(serializer.data)

    
        


@api_view(['POST'])
def insertChargingRequestLog(request):
    data = request.data
    chargingRequestLog = ChargingRequestLog(
            station_id=data["station_id"],
            driver_token=data["driver_token"],
            callback_url=data["callback_url"],
            request_time=data["request_time"],
            decision_time=data["decision_time"],
            decision=data["decision"]
        )
    chargingRequestLog.save(force_insert=True)
    return Response({"status": "Log saved successfully"})

@api_view(['GET'])
def getRequestLog(request):
    from django.db import connection
    connection.close()
    logs = ChargingRequestLog.objects.all()

    # Serialize the queryset
    serializer = ChargingRequestLogSerializer(logs, many=True)

    # Return the JSON response
    return Response(serializer.data)


