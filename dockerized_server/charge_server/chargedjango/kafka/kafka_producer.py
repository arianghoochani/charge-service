from confluent_kafka import Producer
import json
import time

KAFKA_BROKER = "kafka:9092"
TOPIC_NAME = "charging_requests"

producer_conf = {'bootstrap.servers': KAFKA_BROKER}
producer = Producer(producer_conf)

def send_to_kafka(topic, message, retries=3, delay=2):
    try:
        message_json = json.dumps(message)
    except Exception as e:
        print(f" Failed to serialize message: {e}")
        return False

    for attempt in range(retries):
        try:
            producer.produce(topic, message_json)
            producer.flush()
            print(f" Kafka message sent: {message}")
            return True
        except Exception as e:
            logging.warning(f"Kafka attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    
    logging.error(f"Failed to send Kafka message after {retries} attempts.")
    return False
