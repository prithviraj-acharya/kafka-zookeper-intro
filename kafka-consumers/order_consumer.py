import sys
import json
import signal
from kafka import KafkaConsumer

def handle_exit(sig, frame):
    print("\nConsumer shutting down.")
    exit(0)

signal.signal(signal.SIGINT, handle_exit)

print("Usage: python order_consumer.py [group_id]")
group_id = sys.argv[1] if len(sys.argv) > 1 else "order-processor"

consumer = KafkaConsumer(
    'orders',
    bootstrap_servers='localhost:9092',
    group_id=group_id,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

def on_assign(consumer, partitions):
    print(f"Assigned partitions: {[p.partition for p in partitions]}")

consumer.subscribe(['orders'])
consumer.on_partitions_assigned = on_assign

print(f"Consumer started in group: {group_id} (auto_offset_reset=earliest)")
for msg in consumer:
    order = msg.value
    print(
        f"Group: {group_id} | Partition: {msg.partition} | Offset: {msg.offset} | "
        f"age_group: {order.get('age_group')} | order_id: {order.get('_id')}"
    )
