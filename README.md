# FastAPI-Kafka-WebSockets Project

This project demonstrates how to build a real-time web application using FastAPI, Kafka, and WebSockets. The architecture is designed to handle high-throughput data streams from Kafka and deliver real-time updates to clients via WebSockets.

## Components

- **FastAPI**: A modern, fast web framework for building APIs with Python 3.7+.
- **Kafka**: A distributed streaming platform that is used for building real-time data pipelines and streaming applications.
- **WebSockets**: A protocol that provides full-duplex communication channels over a single TCP connection, ideal for real-time updates.

## Features

- **High-Throughput Data Ingestion**: Data from various sources can be ingested into Kafka.
- **Real-Time Data Processing**: FastAPI processes Kafka messages asynchronously and prepares them for client consumption.
- **Real-Time Updates**: WebSocket connections allow clients to receive real-time data updates.

## Prerequisites

- Python 3.7+
- Kafka and Zookeeper (can be set up using Docker)
- Required Python packages (FastAPI, Uvicorn, aiokafka, websockets)

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/0leksandrr/FastAPI-Kafka-WebSockets.git
   cd fastapi-kafka-websockets
