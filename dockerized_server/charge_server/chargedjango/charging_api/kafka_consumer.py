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

# 🔹 Django API URL for inserting logs
DJANGO_API_URL = "http://chargebackend:8000/api/insertchargingrequestlog/"

# 🔹 Add project directory to PYTHONPATH
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "charge_service_project.settings")

# 🔹 Initialize Django (Even if we don’t use ORM)
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

def send_to_django_api(station_id, driver_token, callback_url, request_time, decision):
    """
    Sends the charging request data to Django API for saving.
    """
    try:
        # Convert datetime to string
        if isinstance(request_time, datetime):
            request_time = request_time.isoformat()

        decision_time = now().isoformat()

        payload = {
            "station_id": station_id,
            "driver_token": driver_token,
            "callback_url": callback_url,
            "request_time": request_time,
            "decision_time": decision_time,
            "decision": decision,
        }

        response = requests.post("http://138.199.214.157/api/insertlog/", json=payload)

        if response.status_code == 200:
            print(f"✅ SUCCESS: Log sent to Django API -> {payload}")
        else:
            print(f"❌ ERROR: Django API failed -> {response.status_code} - {response.text}")

    except requests.RequestException as e:
        print(f"❌ ERROR: Failed to send data to Django API -> {e}")


def process_messages():
    print("Kafka Consumer Started... Listening for messages...")
    
    while True:
        msg = consumer.poll(1.0)  # Poll every second

        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
        data = json.loads(msg.value().decode('utf-8'))
        station_id = data.get("station_id")
        driver_token = data.get("driver_token")
        callback_url = data.get("callback_url")
        request_time = parse_datetime(data.get("request_time"))
        response = requests.post("http://138.199.214.157/api/checkauthority/", json={"station_id": station_id, "driver_token": driver_token,"request_time":request_time,"callback_url":callback_url})
        # # ✅ **Correctly Parse Kafka Message**
        # try:
        #     data = json.loads(msg.value().decode('utf-8'))
        #     station_id = data.get("station_id")
        #     driver_token = data.get("driver_token")
        #     callback_url = data.get("callback_url")
        #     request_time = parse_datetime(data.get("request_time"))

           
        #     send_to_django_api(station_id, driver_token, callback_url, request_time)
        #     try:
        #         response = requests.post(callback_url, json={"status": decision})
        #         print(f"✅ Sent callback response: {response.status_code}")
        #     except requests.RequestException as e:
        #         print(f"❌ ERROR: Failed to send callback -> {e}")

        # except Exception as e:
        #     print(f"❌ ERROR: Failed to process Kafka message -> {e}")


if __name__ == "__main__":
    process_messages()



