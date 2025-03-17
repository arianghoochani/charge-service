# charge-service

# Charge Service - Request Handling System 

## Overview

Charge Service is a **fully dockerized** and **scalable** Django-based service designed to handle **electric vehicle (EV) charging authorization** in a **synchronous** manner. The system utilizes **Kafka** for queuing requests and **Django REST Framework (DRF)** to manage API interactions. **NGINX** is used as the web server, and **Docker Compose** ensures a seamless deployment experience, eliminating manual dependency management.

##  Tech Stack

- **Backend**: Django + DRF
- **Queuing**: Apache Kafka
- **Web Server**: NGINX
- **Containerization**: Docker & Docker Compose

---

##  How to Use

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/arianghoochani/charge-service.git
```
### 2️⃣ Update the Docker Configuration

#### Navigate to the `docker-compose.yml` file located in:
```sh
cd charge-service/dockerized_server
```
Modify the Kafka Consumer Service section (line 59):
```sh
  kafka_consumer:
    build:
      context: ./charge_server/chargedjango
    container_name: kafka_consumer
    environment:
      - KAFKA_BROKER=kafka:9092
      - DJANGO_API_URL=http://YOUR_SERVER_IP/api/checkauthority/
    command: sh -c "python kafka/kafka_consumer.py"
    depends_on:
      - kafka-init
      - chargebackend
    volumes:
      - ./charge_server/chargedjango/db.sqlite3:/backend/db.sqlite3

```
Replace http://YOUR_SERVER_IP with your server's actual IP.

### 3️⃣ Build & Run the Service
```sh
docker compose build
docker compose up -d
For older Docker versions:
```
```sh
docker-compose build
docker-compose up -d
```


### API Endpoints

| Endpoint                         | Method | Request Fields | Response Fields | Description |
|----------------------------------|--------|----------------|----------------|-------------|
| `/api/chargingRequestValidator/` | POST   | `station_id`, `driver_token`, `callback_url` | `status`, `message` | Main controller API: Receives charging requests, passes them to internal APIs, and queues them for processing. |
| `/api/checkauthority/`           | POST   | `station_id`, `driver_token`, `request_time`, `callback_url` | `message` | Internal authorization service, **never called directly**. Requests are processed asynchronously via Kafka. |
| `/api/insertACL/`                | POST   | `station_id`, `driver_token` | `flag` | Adds new authorized drivers and stations to allow charging. |
| `/api/getrequestlog/`            | GET    | None           | `id`, `station_id`, `driver_token`, `callback_url`, `request_time`, `decision_time`, `decision` | Retrieves a list of all charging requests, useful for monitoring system activity. |


##  Charge Request Handling System Architecture

This project handles **asynchronous charge authorization** using **Kafka** for queuing. The architecture ensures **scalability, reliability, and efficiency** by separating concerns into distinct components.


###  System Flow:


###  Component Breakdown:

1️⃣ **User/Client**  
   - Sends a **charging request** via an API endpoint.

2️⃣ **Django Backend**  
   - Validates the request.
   - Passes the request to **Kafka Producer** for queuing.

3️⃣ **Kafka Producer**  
   - Pushes the request into a **Kafka Topic (`charging_requests`)**.

4️⃣ **Kafka Consumer (Django)**  
   - Listens to the Kafka queue.
   - Processes messages and checks authorization via **Authorization API**.

5️⃣ **Authorization API**  
   - Determines whether the request is **allowed or denied**.

6️⃣ **Decision Log DB**  
   - Stores request decisions for **future reference and monitoring**.

---


