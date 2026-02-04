# Week 2 – Day 1: Bottlenecks & First Scaling Decisions

## New Assumptions

- Millions of short URLs
- Redirect traffic ≫ create traffic
- Redirect p95 latency target ~10ms

## Redirect Critical Path

1. HTTP request arrives
2. Path parsing and shortened_url extraction
3. SQLite connection creation
4. Disk-backed DB lookup
5. Redirect response returned

## Primary Bottleneck

- Synchronous disk I/O on every redirect request
- SQLite reads on the hot path

## Bottleneck Classification

- IO-bound

## First Optimization Decision

- Introduce in-memory cache for shortened_url → source_url mapping
- Remove disk access from redirect hot path

## Why In-Memory Cache First

- Single-instance system
- Avoids network hop
- Minimal operational complexity
- Reversible decision

## Accepted Risks

- Cache loss on process restart (cold start latency)
- Memory growth without eviction
