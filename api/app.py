from flask import Flask, request, jsonify
from kafka import KafkaProducer, KafkaConsumer
import os, json

app = Flask(__name__)
KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka1:19092")

import uuid
import random

@app.route('/produce', methods=['POST'])
def produce():
    producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    # Generate random order data with age and age_group
    age = random.randint(10, 70)
    if age < 18:
        age_group = 'child'
    elif age < 40:
        age_group = 'adult'
    else:
        age_group = 'senior'
    order = {
        '_id': str(uuid.uuid4()),
        'customer_id': str(uuid.uuid4()),
        'age': age,
        'age_group': age_group,
        'items': [
            {
                'id': str(uuid.uuid4()),
                'quantity': random.randint(1, 5)
            }
            for _ in range(random.randint(1, 3))
        ]
    }
    producer.send('orders', order, key=age_group.encode())
    producer.flush()
    return jsonify({'status': 'random order sent', 'order': order}), 200



@app.route('/')
def index():
    return "Kafka Flask API is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
