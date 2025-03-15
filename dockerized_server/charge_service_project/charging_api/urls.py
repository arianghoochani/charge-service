from django.urls import path,include
from . import views

urlpatterns = [
    path('chargingRequestValidator/',views.chargingRequestValidator,name='chargingRequestValidator'),
    path('getrequestlog/',views.getRequestLog,name='getRequestLog'),
    path('addacl/',views.addACL,name='addACL'),
    ]