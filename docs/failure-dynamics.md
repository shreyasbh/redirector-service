# Failure Dynamics and Concurrency Protection

## 1. Throughput Model

Effective system capacity under blocking dependencies can be approximated as:

Capacity = Workers / HoldTime

Where:

- Workers = number of concurrent worker threads/processes
- HoldTime = time each worker is occupied per request

If HoldTime increases (e.g., slow DB), effective throughput drops even if worker count remains constant.

---

## 2. Queue Growth Model

If:

ArrivalRate > ServiceRate

Then:

QueueGrowthRate = ArrivalRate - ServiceRate

If this condition persists, backlog grows linearly over time.

Once internal queues fill (Gunicorn backlog, OS socket buffer), new requests are dropped or time out.

---

## 3. Nonlinear Collapse in Distributed Systems

When a remote dependency (e.g., Postgres) becomes slow:

1. Workers block longer.
2. Effective throughput drops.
3. Backlog grows.
4. Clients retry.
5. Incoming traffic increases.
6. Downstream load increases further.

This creates a positive feedback loop that can cause nonlinear collapse (congestion amplification).

---

## 4. Role of Timeouts

Timeouts do not increase successful throughput.

They:

- Bound worker occupancy time.
- Prevent long-lived blocking.
- Preserve concurrency capacity.
- Reduce backlog growth.

By failing fast, the system remains responsive even under downstream failure.

---

## 5. Role of Circuit Breakers

Timeouts still allow every request to attempt the dependency.

Circuit breakers:

- Stop sending traffic to an unhealthy downstream service after a failure threshold.
- Cut the positive feedback loop.
- Reduce downstream load.
- Allow the system to stabilize.

They are systemic protection, not optimization.

---

## 6. SQLite vs Postgres — Failure Domains

### SQLite

- Embedded in-process.
- Shared failure domain with application.
- Degradation is typically shared (CPU, disk, memory).
- No independent network latency amplification.

### Postgres (remote)

- Independent failure domain.
- Network latency introduced.
- Partial failure possible (DB slow while app remains healthy).
- Risk of congestion amplification across tiers.
