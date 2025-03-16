from django.db import models


class ChargingRequestLog(models.Model):
    station_id = models.CharField(max_length=36) 
    driver_token = models.CharField(max_length=80) 
    callback_url = models.URLField()  
    request_time = models.DateTimeField(auto_now_add=True) 
    decision_time = models.DateTimeField(null=True, blank=True)  
    decision = models.CharField(
        max_length=20,
        choices=[
            ("allowed", "Allowed"),
            ("not_allowed", "Not Allowed"),
            ("unknown", "Unknown"),
            ("invalid", "Invalid"),
        ],
        default="unknown"
    )

class AccessControlList(models.Model):
    ACL_id = models.CharField(max_length=140,primary_key= True) 
    station_id = models.CharField(max_length=36) 
    driver_token = models.CharField(max_length=80) 
    