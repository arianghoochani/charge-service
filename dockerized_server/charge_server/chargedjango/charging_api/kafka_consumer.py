from confluent_kafka import Consumer
import json
import requests
from django.utils.timezone import now
import os
import sys
import django
from datetime import datetime
from django.utils.dateparse import parse_datetime
# 🔹 Set the correct project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 🔹 Add project directory to PYTHONPATH
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "charge_service_project.settings")

# 🔹 Initialize Django
django.setup()

from charging_api.models import ChargingRequestLog

KAFKA_BROKER = "kafka:9092"
TOPIC_NAME = "charging_requests"

consumer_conf = {
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'acl_service_group',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(consumer_conf)
consumer.subscribe([TOPIC_NAME])

ACL = [
    ("550e8400-e29b-41d4-a716-446655440000", "user-123~valid.token")
]

def process_messages():
    print("Kafka Consumer Started... Listening for messages...")
    
    while True:
        msg = consumer.poll(1.0)  # Poll every second

        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        # Parse message
        data = json.loads(msg.value().decode('utf-8'))
        station_id = data["station_id"]
        driver_token = data["driver_token"]
        callback_url = data["callback_url"]
        # request_time = data["request_time"]

        decision = "allowed" if (station_id, driver_token) in ACL else "not_allowed"

        request_time = parse_datetime(data["request_time"])
        if request_time is None:
           request_time = now()  # Use current time if parsing fails
        chargingRequestLog = ChargingRequestLog(station_id= station_id,driver_token=driver_token,callback_url= callback_url,request_time=request_time,decision_time= now(),decision=decision)
        chargingRequestLog.save(force_insert=True)
       
        response = requests.post(callback_url, json={"status": decision})
        print(f"Sent callback response: {response.status_code}")

        # except ChargingRequestLog.DoesNotExist:
        #     print(f"No matching record found for {station_id}, {driver_token}")

if __name__ == "__main__":
    process_messages()
