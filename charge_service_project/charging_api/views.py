from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ChargingRequestValidatorSerializer
@api_view(['GET'])
def chargingRequestValidator(request):
    f = {}
    try:
        serializer = ChargingRequestValidatorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        f = {"message":"ok"}
    except:
        f = {"message":"error"}
    return Response f