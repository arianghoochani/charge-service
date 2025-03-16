import sqlite3
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

# 🔹 SQLite Database Path
DB_PATH = os.path.join(BASE_DIR, "db.sqlite3")

# 🔹 Add project directory to PYTHONPATH
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "charge_service_project.settings")

# 🔹 Initialize Django (Even if we don’t use ORM)
django.setup()

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

def insert_into_db(station_id, driver_token, callback_url, request_time, decision):
    """
    Inserts data directly into SQLite database without using Django ORM.
    """
    try:
        conn = sqlite3.connect(DB_PATH)  # Connect to SQLite
        cursor = conn.cursor()

        # 🔹 Convert request_time to string if needed
        if isinstance(request_time, datetime):
            request_time = request_time.isoformat()

        decision_time = now().isoformat()

        # 🔹 Insert query
        cursor.execute("""
            INSERT INTO charging_api_chargingrequestlog 
            (station_id, driver_token, callback_url, request_time, decision_time, decision) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (station_id, driver_token, callback_url, request_time, decision_time, decision))

        conn.commit()  # Save changes
        conn.close()  # Close connection
        print(f"✅ SUCCESS: Manually inserted record -> {station_id}, {driver_token}")

    except sqlite3.Error as e:
        print(f"❌ ERROR: SQLite Insert Failed -> {e}")


def process_messages():
    print("Kafka Consumer Started... Listening for messages...")
    
    while True:
        msg = consumer.poll(1.0)  # Poll every second

        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        # ✅ **Correctly Parse Kafka Message**
        try:
            data = json.loads(msg.value().decode('utf-8'))
            station_id = data.get("station_id")
            driver_token = data.get("driver_token")
            callback_url = data.get("callback_url")
            request_time = parse_datetime(data.get("request_time"))

            if request_time is None:
                request_time = now()  # Use current time if parsing fails

            decision = "allowed" if (station_id, driver_token) in ACL else "not_allowed"

            #  **Insert into SQLite manually**
            insert_into_db(station_id, driver_token, callback_url, request_time, decision)

            #  **Send decision to callback URL**
            try:
                response = requests.post(callback_url, json={"status": decision})
                print(f"Sent callback response: {response.status_code}")
            except requests.RequestException as e:
                print(f" ERROR: Failed to send callback -> {e}")

        except Exception as e:
            print(f" ERROR: Failed to process Kafka message -> {e}")


if __name__ == "__main__":
    process_messages()


# from confluent_kafka import Consumer
# import json
# import requests
# from django.utils.timezone import now
# import os
# import sys
# import django
# from datetime import datetime
# from django.utils.dateparse import parse_datetime
# # 🔹 Set the correct project base directory
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# # 🔹 Add project directory to PYTHONPATH
# sys.path.append(BASE_DIR)
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "charge_service_project.settings")

# # 🔹 Initialize Django
# django.setup()

# from charging_api.models import ChargingRequestLog

# KAFKA_BROKER = "kafka:9092"
# TOPIC_NAME = "charging_requests"

# consumer_conf = {
#     'bootstrap.servers': KAFKA_BROKER,
#     'group.id': 'acl_service_group',
#     'auto.offset.reset': 'earliest'
# }
# consumer = Consumer(consumer_conf)
# consumer.subscribe([TOPIC_NAME])

# ACL = [
#     ("550e8400-e29b-41d4-a716-446655440000", "user-123~valid.token")
# ]

# def process_messages():
#     print("Kafka Consumer Started... Listening for messages...")
    
#     while True:
#         msg = consumer.poll(1.0)  # Poll every second

#         if msg is None:
#             continue
#         if msg.error():
#             print(f"Consumer error: {msg.error()}")
#             continue

#         # Parse message
#         data = json.loads(msg.value().decode('utf-8'))
#         station_id = data["station_id"]
#         driver_token = data["driver_token"]
#         callback_url = data["callback_url"]
#         # request_time = data["request_time"]

#         decision = "allowed" if (station_id, driver_token) in ACL else "not_allowed"

#         request_time = parse_datetime(data["request_time"])
#         if request_time is None:
#            request_time = now()  # Use current time if parsing fails
#         # 🔹 DEBUG: Print values before saving
#         print(f"📌 DEBUG: Attempting to save log -> {station_id}, {driver_token}, {decision}")

#         try:
#             chargingRequestLog = ChargingRequestLog(
#                 station_id=station_id,
#                 driver_token=driver_token,
#                 callback_url=callback_url,
#                 request_time=request_time,
#                 decision_time=now(),
#                 decision=decision
#             )
#             chargingRequestLog.save(force_insert=True)
#             print("✅ SUCCESS: Log saved!")

#         except Exception as e:
#             print(f"❌ ERROR: Could not save log -> {e}")
       
#         response = requests.post(callback_url, json={"status": decision})
#         print(f"Sent callback response: {response.status_code}")

#         # except ChargingRequestLog.DoesNotExist:
#         #     print(f"No matching record found for {station_id}, {driver_token}")

# if __name__ == "__main__":
#     process_messages()
