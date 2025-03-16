from django.urls import path,include
from . import views

urlpatterns = [
    path('chargingRequestValidator/',views.chargingRequestValidator,name='chargingRequestValidator'),
    path('getrequestlog/',views.getRequestLog,name='getRequestLog'),
    path('insertACL/',views.insertACL,name='insertACL'),
    path('checkauthority/',views.checkAuthority,name='checkAuthority'),
    ]