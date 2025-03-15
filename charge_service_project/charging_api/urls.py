from django.urls import path,include
from . import views

urlpatterns = [
    path('chargingRequestValidator/',views.chargingRequestValidator,name='chargingRequestValidator'),
    ]