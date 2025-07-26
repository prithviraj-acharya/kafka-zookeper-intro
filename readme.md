# 🌀 Kafka Streaming Playground

A modern, hands-on Kafka demo stack for real-time data streaming, analytics, and visualization. Includes:

- Real-time message production & consumption
- Multi-partition topics, multiple consumer groups
- Kafka UI for live topic/consumer inspection
- Flask-based HTTP API producer
- ksqlDB for streaming SQL (windowing, joins, aggregations)
- Lightweight HTML/JS dashboard for offsets, lag, and message flow

---

## 📦 Project Structure

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

| Endpoint        | Method | Description                            |
| --------------- | ------ | -------------------------------------- |
| `/produce`      | POST   | Send a message to Kafka topic `events` |
| `/offsets`      | GET    | Returns end offsets and consumer lag   |
| `/messages`     | GET    | Returns recent messages from DB        |
| `/stream-table` | GET    | (optional) ksqlDB query results        |
| `/`             | GET    | HTML dashboard                         |

---

## 📊 Dashboard Features

- Live **offsets and lag** bar chart per partition
- Real-time **tail of recent messages**
- Simple **producer input** to send new messages
- (Optional) ksqlDB query results

---

## 🧪 Sample ksqlDB Queries

**Create a Stream on Topic `events`:**
```sql
CREATE STREAM events_raw (
    msg VARCHAR
) WITH (
    KAFKA_TOPIC='events',
    VALUE_FORMAT='JSON'
);
```

**Group & Count by Prefix:**
```sql
CREATE TABLE msg_count AS
  SELECT SUBSTRING(msg, 0, 5) AS prefix,
         COUNT(*) AS total
  FROM events_raw
  GROUP BY prefix
  EMIT CHANGES;
```

**Windowed Aggregation (1-minute):**
```sql
CREATE TABLE msg_per_min AS
  SELECT msg, COUNT(*) AS count
  FROM events_raw
  WINDOW TUMBLING (SIZE 1 MINUTE)
  GROUP BY msg
  EMIT CHANGES;
```

---

## 🧪 Experiments

- Start multiple consumers in the **same group** → observe rebalance
- Start consumers with **different group IDs** → each gets full stream
- Watch **lag** live in Kafka UI or dashboard
- Run **ksqlDB JOINs** between 2 streams
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

## 🤝 License

MIT or Apache-2.0 — use freely for learning or demos!
