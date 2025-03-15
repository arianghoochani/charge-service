from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ChargingRequestValidatorSerializer
@api_view(['GET'])
def chargingRequestValidator(request):
    return Response("hello")