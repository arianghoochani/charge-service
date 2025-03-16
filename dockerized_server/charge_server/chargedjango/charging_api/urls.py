from django.urls import path,include
from . import views

urlpatterns = [
    path('chargingRequestValidator/',views.chargingRequestValidator,name='chargingRequestValidator'),
    path('insertlog/',views.insertChargingRequestLog,name='insertChargingRequestLog'),
    path('addacl/',views.addACL,name='addACL'),
    ]