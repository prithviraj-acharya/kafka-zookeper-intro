
# 🌀 Kafka Streaming Playground: Real-Time Order Processing Demo

A modern, hands-on Kafka demo stack for real-time data streaming, analytics, and visualization, modeled as a simple **Order Processing System**. Includes:

- Real-time order creation & processing
- Multi-partition topics, multiple consumer groups (e.g., order processor, analytics)
- Kafka UI for live topic/consumer inspection
- Flask-based HTTP API for order submission
- ksqlDB for streaming SQL (windowing, joins, aggregations)
- Lightweight HTML/JS dashboard for offsets, lag, and message flow

---


---

## � Real-Life Scenario: Order Processing System

**Actors:**
- Users place orders (via API or dashboard)
- Multiple services (consumers) process orders for different purposes

**Flow:**
1. **Order Producer:**
   - Users submit new orders via the `/produce` API (or dashboard form).
   - Each order is a JSON message (e.g., `{ "order_id": 123, "user": "alice", "item": "book", "qty": 2 }`).
   - Orders are sent to the Kafka topic `orders` (with multiple partitions).
2. **Multiple Consumer Groups:**
   - **Order Processor Group:** Consumes orders and marks them as processed.
   - **Analytics Group:** Consumes orders to update real-time stats (e.g., top items, sales per minute).
   - Each group tracks its own offsets.
3. **Offset & Lag Tracking:**
   - Dashboard and `/offsets` API show how many orders are pending for each group.
4. **ksqlDB:**
   - Run streaming SQL to aggregate orders (e.g., count orders per item per minute).

---

## �📦 Project Structure

```
.
├── docker-compose.yml      # Launches Kafka, ZooKeeper, Kafka UI, API, ksqlDB
├── api/                    # Python Flask API (producer & consumer)
│   ├── app.py
│   └── requirements.txt
├── dashboard/              # HTML/JS frontend for Kafka internals
│   └── index.html
├── init/
│   └── ksql-init.sql       # (Optional) Pre-load ksqlDB streams/tables
```

---

## 🚀 Quick Start

1. **Clone & Launch**
   ```bash
   git clone https://github.com/prithviraj-acharya/kafka-zookeper-intro.git
   cd kafka-streaming-playground
   docker-compose up --build -d
   ```
2. **Open Kafka UI**
   - Visit [http://localhost:8080](http://localhost:8080)
   - Explore topics, partitions, consumer groups, offsets, and lag in real time

---

## 🧩 Services

| Service       | Description                                 |
| ------------- | ------------------------------------------- |
| ZooKeeper     | Kafka coordination layer                    |
| Kafka Broker  | Message broker, partitioned log store       |
| Kafka UI      | Web-based viewer for topics, consumers      |
| Flask API     | HTTP message producer (and consumer logic)  |
| ksqlDB Server | Streaming SQL engine over Kafka topics      |
| Dashboard     | HTML/JS UI to visualize Kafka internals     |

---

## 🎯 Kafka Concepts

- **Multiple partitions** per topic
- **Multiple consumer groups** (independent offsets)
- **Consumer rebalancing** and lag tracking
- Message production via **HTTP API**
- **ksqlDB streams/tables**: filtering, joins, windowing, materialized views

---


## 🔁 API Endpoints

| Endpoint        | Method | Description                                 |
| --------------- | ------ | ------------------------------------------- |
| `/produce`      | POST   | Submit a new order to Kafka topic `orders`  |
| `/offsets`      | GET    | Returns end offsets and consumer lag        |
| `/messages`     | GET    | Returns recent orders from DB or Kafka      |
| `/stream-table` | GET    | (optional) ksqlDB query results             |
| `/`             | GET    | HTML dashboard                              |

---


## 📊 Dashboard Features

- Live **offsets and lag** bar chart per partition
- Real-time **tail of recent orders**
- Simple **order input** to send new orders
- (Optional) ksqlDB query results

---

## 🧪 Sample ksqlDB Queries


**Create a Stream on Topic `orders`:**
```sql
CREATE STREAM orders_raw (
    order_id INT,
    user VARCHAR,
    item VARCHAR,
    qty INT
) WITH (
    KAFKA_TOPIC='orders',
    VALUE_FORMAT='JSON'
);
```

**Group & Count by Item:**
```sql
CREATE TABLE item_count AS
  SELECT item, COUNT(*) AS total
  FROM orders_raw
  GROUP BY item
  EMIT CHANGES;
```

**Windowed Aggregation (1-minute):**
```sql
CREATE TABLE orders_per_min AS
  SELECT item, COUNT(*) AS count
  FROM orders_raw
  WINDOW TUMBLING (SIZE 1 MINUTE)
  GROUP BY item
  EMIT CHANGES;
```

---


## 🧪 Experiments

- Start multiple consumers in the **Order Processor group** → observe rebalance
- Start consumers with **different group IDs** (e.g., analytics) → each gets full stream
- Watch **lag** live in Kafka UI or dashboard
- Run **ksqlDB JOINs** between 2 streams (e.g., orders and users)
- Add new topics, producers, or windowed aggregations

---

## 🛠️ Prerequisites

- Docker & Docker Compose
- (Optional) Python 3 (`pip install kafka-python flask`)
- (Optional) SQLite browser or CLI

---

## 📚 References

- [Kafka Documentation](https://kafka.apache.org/documentation/)
- [ksqlDB Documentation](https://docs.confluent.io/ksqldb/)
- [Kafka UI (Provectus)](https://github.com/provectus/kafka-ui)

---


## 📌 To-Do / Enhancements

- [ ] Add Kafka Connect (sink to Postgres / Mongo)
- [ ] Add authentication (SASL_SSL)
- [ ] Add monitoring via Prometheus/Grafana
- [ ] Deploy on Kubernetes (Helm or Compose on K8s)

---

## 📝 Step-by-Step Plan

1. **Create Kafka topic `orders` with multiple partitions**
   - Use Kafka CLI or UI to create the topic before running the app. - DONE
2. **Implement order producer endpoint (`/produce`)**
   - Accept order JSON and send to Kafka topic. - DONE
3. **Implement order consumer(s)**
   - Create consumer logic for at least two groups: order processor and analytics.
   - Use `age` and `age_group` fields in the order data to experiment with partitioning (e.g., use `age_group` as the Kafka message key).
   - Optionally expose `/messages` endpoint to fetch recent orders.
4. **Add offset and lag tracking**
   - Implement `/offsets` endpoint and dashboard visualization.
5. **Integrate ksqlDB for real-time analytics**
   - Use provided SQL to create streams/tables for aggregations.
6. **Test with multiple consumers and groups**
   - Observe rebalancing and lag in UI and dashboard.
7. **(Optional) Extend with more features**
   - Add more endpoints, dashboards, or ksqlDB queries as needed.

---

## 🤝 License

MIT or Apache-2.0 — use freely for learning or demos!
