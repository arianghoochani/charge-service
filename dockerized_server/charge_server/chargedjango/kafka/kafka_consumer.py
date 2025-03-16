from confluent_kafka import Consumer
import json
import requests
from datetime import datetime
from django.utils.dateparse import parse_datetime


KAFKA_BROKER = "kafka:9092"
TOPIC_NAME = "charging_requests"

consumer_conf = {
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'acl_service_group',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(consumer_conf)
consumer.subscribe([TOPIC_NAME])




def process_messages():
    print("Kafka Consumer Started... Listening for messages...")
    
    while True:
        msg = consumer.poll(5.0)  # Poll every 5 second

        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
        try:
            data = json.loads(msg.value().decode('utf-8'))
            station_id = data.get("station_id")
            driver_token = data.get("driver_token")
            callback_url = data.get("callback_url")
            request_time = parse_datetime(data.get("request_time"))
            if request_time is not None:
                request_time = request_time.isoformat()
            response = requests.post("http://138.199.214.157/api/checkauthority/", json={"station_id": station_id, "driver_token": driver_token,"request_time":request_time,"callback_url":callback_url})
        except Exception as e:
            print(f"Error occurred while processing message: {e}")
            continue
       

if __name__ == "__main__":
    process_messages()



