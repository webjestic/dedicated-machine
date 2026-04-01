# Rate Limiter — Operational Design Document

**Version:** 1.0-draft
**Status:** Pending decision point resolution (see §7)
**Audience:** Implementing engineer, on-call rotation, infrastructure team

---

## 1. Overview

### What This System Does

This system is a configurable, Redis-backed rate limiter implemented as a Node.js middleware library and/or standalone service. It enforces request rate limits on a per-identifier basis (e.g., IP address, API key, user ID) using a sliding window algorithm backed by Redis. When a client exceeds its configured limit, the system returns a structured 429 response with enough information for the client to back off correctly.

### What This System Does Not Do

- **It does not authenticate requests.** The identifier used for rate limiting is passed in or extracted from an already-parsed request. Identity verification is out of scope.
- **It does not perform IP geolocation or threat scoring.** It counts requests. Nothing more.
- **It does not manage Redis infrastructure.** It consumes a Redis connection; it does not own it.
- **It does not provide per-route or per-method differentiation** unless the calling application constructs distinct identifiers or limit configurations per route. The limiter itself is identifier-agnostic.
- **It does not replace a WAF or DDoS mitigation layer.** It is a correctness and fairness control, not a security perimeter.
- **It does not persist limit configurations.** Limits are supplied at initialization time via configuration. Dynamic limit changes require a process restart unless the implementation engineer adds a configuration reload path (see §8).

### Assumptions

1. Redis is available as a shared, persistent store accessible to all Node.js process instances. If multiple instances of the application run behind a load balancer, they all point to the same Redis instance or cluster.
2. The Node.js application sits behind a reverse proxy (nginx, AWS ALB, Cloudflare, etc.). The real client IP must be extracted from `X-Forwarded-For` or a trusted header — not `req.socket.remoteAddress`, which will be the proxy IP. **This extraction logic must be implemented and audited before deployment.** See §7, Decision Point D-03.
3. System clocks across application nodes are synchronized via NTP. Clock skew greater than 1 second is considered a misconfiguration.
4. Redis latency is expected to be under 5ms p99 under normal operating conditions. The rate limiter adds this latency to every request in the hot path.
5. The implementing engineer has access to a metrics emission interface (StatsD, Prometheus client, etc.). The specific backend is a decision point (D-05).

---

## 2. Algorithm

### Selected Algorithm: Sliding Window Log (Redis-backed with approximation fallback)

**Primary:** Sliding Window Counter (approximated via two fixed windows)
**Rationale and tradeoffs follow.**

### Algorithm Options Considered

| Algorithm | Pros | Cons |
|---|---|---|
| Fixed Window Counter | Simple, O(1) memory per key | Burst vulnerability at window boundary (2x burst possible) |
| Sliding Window Log | Perfectly accurate | O(n) memory per key per window; unbounded under attack |
| Sliding Window Counter (approximated) | O(1) memory, near-accurate, no burst boundary | ~10% error at window boundary; acceptable for most use cases |
| Token Bucket | Smooth burst handling | Complex distributed state; harder to reason about under Redis failure |
| Leaky Bucket | Strict output rate | Does not map naturally to request/response; adds queue complexity |

### Selected Algorithm: Approximated Sliding Window Counter

**Specification:**

Given:
- `limit` = maximum requests allowed per window
- `window_size` = window duration in seconds
- `now` = current Unix timestamp in seconds
- `current_window` = `floor(now / window_size)`
- `previous_window` = `current_window - 1`
- `elapsed_fraction` = `(now % window_size) / window_size`

**Count calculation:**

```
current_count  = GET counter for current_window key
previous_count = GET counter for previous_window key
weighted_count = previous_count * (1 - elapsed_fraction) + current_count
```

If `weighted_count >= limit`, the request is rejected.
If `weighted_count < limit`, increment `current_count` and allow the request.

**Why this algorithm:**

The fixed window counter is disqualified because a client can make `2 * limit` requests in a short burst straddling a window boundary. The sliding window log is disqualified because it stores one entry per request — under a sustained attack or a high-volume legitimate client, memory consumption is unbounded. The approximated sliding window counter provides O(1) memory per key, eliminates the boundary burst problem to within ~10% error, and maps cleanly to atomic Redis operations.

**Atomicity:**

The increment and expiry operations for the current window key **must** be executed as a single atomic unit. This must be implemented as a Lua script executed via `EVAL` or `EVALSHA`. A non-atomic read-then-write implementation will produce incorrect counts under concurrent load and is not acceptable.

**Lua script (normative):**

```lua
local current_key   = KEYS[1]
local previous_key  = KEYS[2]
local limit         = tonumber(ARGV[1])
local window_size   = tonumber(ARGV[2])
local now           = tonumber(ARGV[3])
local elapsed_frac  = tonumber(ARGV[4])

local current_count  = tonumber(redis.call('GET', current_key) or 0)
local previous_count = tonumber(redis.call('GET', previous_key) or 0)
local weighted       = previous_count * (1 - elapsed_frac) + current_count

if weighted >= limit then
  return {0, current_count, previous_count, weighted}
end

local new_count = redis.call('INCR', current_key)
if new_count == 1 then
  redis.call('EXPIRE', current_key, window_size * 2)
end

return {1, new_count, previous_count, weighted}
```

Return value index 0: `1` = allowed, `0` = rejected.
Return value index 1: current window count after increment.
Return value index 2: previous window count.
Return value index 3: weighted count used for decision.

**The implementing engineer must not alter the logic of this script without re-running the load test suite defined in §6.5.**

---

## 3. Storage

### Redis Data Structure

**Type:** String (integer counter)
**Operations:** `GET`, `INCR`, `EXPIRE` (via Lua script as specified in §2)

### Key Strategy

```
ratelimit:{namespace}:{identifier}:{window_id}
```

| Component | Description | Example |
|---|---|---|
| `ratelimit:` | Static prefix. Enables Redis keyspace filtering and `SCAN` operations scoped to this system. | `ratelimit:` |
| `{namespace}` | Logical grouping. Typically the application name or route group. Allows multiple independent limiters in one Redis instance. | `api`, `auth`, `webhooks` |
| `{identifier}` | The entity being limited. IP address, API key, user ID. Must be normalized before use (see §8, Note N-02). | `user:8821`, `ip:203.0.113.42` |
| `{window_id}` | Integer: `floor(unix_timestamp / window_size)`. Changes each window period. | `1718400` |

**Example keys for a 60-second window, user 8821, at time 1718400045:**
```
ratelimit:api:user:8821:28640      ← current window  (floor(1718400045/60) = 28640000... wait, recalculate)
ratelimit:api:user:8821:28640000   ← current window
ratelimit:api:user:8821:28639999   ← previous window
```

*Note to implementing engineer: compute `window_id` as `Math.floor(Date.now() / 1000 / window_size_in_seconds)` where `Date.now()` returns milliseconds. Verify this arithmetic in a unit test with fixed timestamps before shipping.*

### TTL

Each key's TTL is set to `window_size * 2` seconds at the moment of first write (`INCR` returns 1). This ensures:
- The previous window key is still readable when needed for the weighted calculation.
- Keys expire automatically; no manual cleanup is required.
- A key that is never written to (i.e., the client never makes a second request in a window) does not accumulate.

**TTL is set only on first write.** The Lua script checks `if new_count == 1` before calling `EXPIRE`. This avoids resetting the TTL on every request, which would prevent keys from expiring under sustained traffic.

### Memory Implications

**Per-key memory cost:** approximately 60–80 bytes per active key (Redis string overhead + key string).

**Estimation formula:**
```
memory_bytes = active_unique_identifiers * 2 * 80
```
(Factor of 2 accounts for current and previous window keys.)

**Example:** 100,000 active unique IPs = ~16 MB. This is negligible on any modern Redis instance, but the estimate should be validated against actual identifier cardinality before production deployment.

**Attack surface:** An adversary who can forge arbitrary identifiers (e.g., spoofed `X-Forwarded-For` headers) can cause unbounded key creation. Identifier extraction must be hardened (§7, D-03) and Redis memory limits must be configured with an eviction policy. See §4, Failure Mode F-05.

### Redis Configuration Requirements

- **`maxmemory-policy`**: Must **not** be set to `noeviction` if there is any risk of memory exhaustion. Recommended: `allkeys-lru`. The implementing engineer must confirm this with the infrastructure team.
- **`hz`**: Default (10) is acceptable. No special tuning required.
- **Persistence**: RDB or AOF persistence is **not required** for rate limiter keys. Loss of rate limit counters on Redis restart is acceptable — it is preferable to a Redis restart blocking traffic. If Redis is shared with other data that requires persistence, this must be coordinated with the infrastructure team.
- **Redis version**: 3.2 or later required for `EVALSHA` and atomic Lua execution guarantees relied upon by this design.

---

## 4. Failure Modes

Each failure mode is specified with: trigger condition, system behavior, and rationale.

**⚠️ Decision Point D-01 (fail-open vs. fail-closed) applies to F-01, F-02, F-03. See §7 before implementing.**

---

### F-01 — Redis Connection Unavailable

**Trigger:** The Redis client cannot establish or maintain a connection. `connect` errors, `ECONNREFUSED`, `ETIMEDOUT`.

**Specified behavior (pending D-01):**
- **Fail-open (default recommendation):** Allow all requests through. Log a `WARN`-level event per request (rate-limited to one log line per second to prevent log flooding). Emit `ratelimit.redis.unavailable` counter metric. Do not return 429 to any client.
- **Fail-closed (alternative):** Return 503 Service Unavailable to all requests. Include `Retry-After: 10` header. Log as above.

**Rationale for recommending fail-open:** A Redis outage should not take down the application. Rate limiting is a fairness and abuse-prevention control; its temporary absence is less harmful than a complete service outage. However, if this rate limiter is the primary defense against credential stuffing or account takeover, fail-closed may be appropriate for specific endpoints.

**Implementation requirement:** The Redis client must be configured with a connection timeout of no more than 200ms and must not block the Node.js event loop during reconnection attempts. Use a non-blocking Redis client (e.g., `ioredis`) with `lazyConnect: true` and `enableOfflineQueue: false`. The offline queue must be disabled so that queued commands do not execute in a burst when Redis reconnects, producing a false "all clear" on stale data.

---

### F-02 — Redis Command Timeout

**Trigger:** Redis is reachable but the `EVAL` command does not return within the configured timeout (recommended: 100ms).

**Specified behavior:** Same as F-01 (fail-open or fail-closed per D-01). The timeout must be enforced client-side using `ioredis` command timeout configuration, not relied upon from the Redis server side. Log `ratelimit.redis.timeout` counter metric separately from `ratelimit.redis.unavailable` — these are distinct failure modes with distinct causes.

---

### F-03 — Redis Returns Unexpected Data

**Trigger:** The Lua script returns a value that cannot be parsed as the expected array structure (e.g., Redis version mismatch, script eviction, corrupted response).

**Specified behavior:** Log an `ERROR`-level event with the raw Redis response. Apply fail-open or fail-closed behavior per D-01. Do not crash the process. Do not surface internal error details to the client.

---

### F-04 — Clock Skew Between Application Nodes

**Trigger:** Two application nodes disagree on the current time by more than 1 second.

**Specified behavior:** The system has no active defense against clock skew — it relies on NTP synchronization (see §1, Assumption 3). If clock skew is detected via monitoring (see §6.1), alert the infrastructure team. The symptom will be inconsistent rate limit enforcement: a client may be allowed more requests than the configured limit because two nodes compute different `window_id` values.

**Detection:** Emit the current `window_id` as a metric tag or log field. Divergence across nodes is detectable in aggregated logs.

---

### F-05 — Redis Memory Exhaustion

**Trigger:** Redis reaches its `maxmemory` limit.

**Specified behavior:** If `allkeys-lru` eviction is configured (required, see §3), Redis will evict the least-recently-used keys, which will be old rate limit windows. This is acceptable — an evicted key is treated as a zero count, which is equivalent to a fresh window for that client. The system continues operating with slightly reduced accuracy.

If `noeviction` is configured, Redis will return errors on write operations. This degrades to F-03 behavior. **This is why `noeviction` is prohibited.**

---

### F-06 — Identifier Extraction Failure

**Trigger:** The identifier cannot be extracted from the request (missing header, malformed value, null).

**Specified behavior:** This must be a hard configuration error surfaced at startup or middleware initialization, not at request time. If the identifier extractor function returns `null` or `undefined` at request time, log an `ERROR` and **fail-open for that specific request** (do not apply rate limiting). Do not use a fallback identifier silently — silent fallback would cause all unidentifiable clients to share a single rate limit bucket, which is a correctness failure.

---

### F-07 — Lua Script Eviction from Redis Script Cache

**Trigger:** Redis evicts the cached Lua script (this can happen on Redis restart or under memory pressure with `script flush`).

**Specified behavior:** Use `EVALSHA` for performance, but catch `NOSCRIPT` errors and fall back to `EVAL` with the full script body. Re-cache the script SHA after successful `EVAL`. This must be implemented. An unhandled `NOSCRIPT` error will cause every rate limit check to fail, degrading to F-03 behavior.

---

### F-08 — Application Process Restart / Deploy

**Trigger:** Rolling deploy or crash-restart of application nodes.

**Specified behavior:** No special handling required. Rate limit state lives in Redis, not in process memory. A restarted process reconnects to Redis and resumes correct operation. Window counters are unaffected.

---

## 5. API Contract

This section defines the contract for the rate limiter as middleware. The "request" is an internal function call; the "response" is the HTTP response emitted when a limit is exceeded.

### Middleware Interface

```
rateLimiter(options) → Express/Node.js middleware function (req, res, next)
```

**Options object (all fields required unless marked optional):**

| Field | Type | Description |
|---|---|---|
| `namespace` | `string` | Logical namespace for key isolation. No spaces. Max 64 chars. |
| `limit` | `number` | Maximum requests allowed per window. Positive integer. |
| `windowSizeSeconds` | `number` | Window duration in seconds. Positive integer. |
| `identifierFn` | `(req) => string \| null` | Function that extracts the rate limit identifier from the request. Must be pure and synchronous. |
| `redisClient` | `ioredis.Redis` | Pre-constructed ioredis client. The rate limiter does not own this connection. |
| `onLimitExceeded` | `(req, res, limitInfo) => void` | Optional. Override the default 429 response handler. |
| `failOpen` | `boolean` | Required. Explicit declaration of fail-open (`true`) or fail-closed (`false`) behavior. No default. Forces the operator to make a conscious choice. |

### Allowed Request (limit not exceeded)

The middleware calls `next()`. The following headers are added to the response:

| Header | Value | Description |
|---|---|---|
| `X-RateLimit-Limit` | `{limit}` | The configured maximum requests per window. |
| `X-RateLimit-Remaining` | `{limit - weighted_count}` | Approximate remaining requests in the current window. Floor at 0. |
| `X-RateLimit-Reset` | Unix timestamp (seconds) | When the current window expires. `(current_window + 1) * window_size`. |
| `X-RateLimit-Window` | `{windowSizeSeconds}` | Window size in seconds. Allows clients to compute retry timing without guessing. |

### Rejected Request (limit exceeded) — HTTP 429

**Status code:** `429 Too Many Requests`

**Required response headers:**

| Header | Value | Notes |
|---|---|---|
| `Retry-After` | Integer seconds | `ceil((current_window + 1) * window_size - now)`. This is the authoritative backoff signal. Must be present. RFC 6585 compliant. |
| `X-RateLimit-Limit` | `{limit}` | |
| `X-RateLimit-Remaining` | `0` | Always 0 on rejection. |
| `X-RateLimit-Reset` | Unix timestamp | Same calculation as above. |
| `X-RateLimit-Window` | `{windowSizeSeconds}` | |
| `Content-Type` | `application/json` | |

**Response body:**

```json
{
  "error": "rate_limit_exceeded",
  "message": "Too many requests. Please retry after the indicated delay.",
  "retryAfter": 42,
  "limit": 100,
  "window": 60
}
```

**Requirements:**
- `retryAfter` in the body must match the `Retry-After` header value exactly.
- The body must not include the client's identifier, internal key names, Redis state, or stack traces.
- The `message` field must be human-readable and actionable. It must not say "rate limited" without telling the client what to do.

### Redis Unavailable — Fail-Closed Path Only

**Status code:** `503 Service Unavailable`

```json
{
  "error": "service_unavailable",
  "message": "Rate limiting is temporarily unavailable. Please retry shortly.",
  "retryAfter": 10
}
```

`Retry-After: 10` header must be present.

---

## 6. Operational Requirements

### 6.1 Observability

#### Metrics

All metrics must be emitted on every request, not only on rejection. The metrics backend is a decision point (D-05), but the metric names and semantics are normative.

| Metric Name | Type | Tags | Description |
|---|---|---|---|
| `ratelimit.request.total` | Counter | `namespace`, `result:[allowed\|rejected\|error]` | Every request evaluated by the limiter. |
| `ratelimit.request.allowed` | Counter | `namespace` | Requests that passed the limit check. |
| `ratelimit.request.rejected` | Counter | `namespace` | Requests that exceeded the limit (429 returned). |
| `ratelimit.redis.latency_ms` | Histogram | `namespace` | Latency of the Redis Lua script execution in milliseconds. Buckets: 1, 5, 10, 25, 50, 100, 250, 500. |
| `ratelimit.redis.error` | Counter | `namespace`, `error_type:[timeout\|unavailable\|unexpected]` | Redis operation failures. |
| `ratelimit.redis.script_miss` | Counter | `namespace` | NOSCRIPT errors caught and recovered (F-07). |
| `ratelimit.failopen.request` | Counter | `namespace` | Requests allowed due to fail-open behavior during Redis failure. |
| `ratelimit.identifier.missing` | Counter | `namespace` | Requests where identifierFn returned null (F-06). |

**Histogram percentiles that must be available in dashboards:** p50, p95, p99, p99.9 of `ratelimit.redis.latency_ms`.

#### Structured Logging

All log events must be structured JSON. The following fields are required on every rate limiter log event:

```json
{
  "timestamp": "ISO8601",
  "level": "INFO|WARN|ERROR",
  "component": "ratelimit",
  "namespace": "...",
  "identifier": "...",
  "result": "allowed|rejected|error|failopen",
  "weighted_count": 94.3,
  "limit": 100,
  "window_id": 28640000,
  "redis_latency_ms": 2.1,
  "request_id": "..."
}
```

**Identifier must be logged.** This is required for incident investigation. If the identifier contains PII (e.g., email addresses used as API keys), the logging pipeline must hash or mask it before storage. This is an infrastructure concern, not a rate limiter concern, but the implementing engineer must flag it to the operator.

**Log volume management:** `INFO`-level logging of every allowed request will be high-volume. The implementing engineer should confirm with the operator whether allowed-request logs are required or whether only rejections and errors should be logged at `INFO`. Rejections and errors must always be logged regardless.

#### Degraded State Definition

The system is in a **degraded state** when any of the following are true:
- `ratelimit.redis.error` rate exceeds 1% of `ratelimit.request.total` over a 1-minute window.
- `ratelimit.redis.latency_ms` p99 exceeds 50ms over a 5-minute window.
- `ratelimit.failopen.request` is non-zero (any fail-open traffic indicates Redis is unhealthy).

---

### 6.2 Graceful Degradation

Graceful degradation behavior is fully specified in §4 (Failure Modes). This section summarizes the operational contract.

**The rate limiter must never crash the Node.js process.** All Redis errors must be caught within the middleware and handled per the fail-open/fail-closed configuration. Unhandled promise rejections from Redis operations are a defect.

**The rate limiter must never block the event loop.** Redis operations are async. The Lua script execution is a single round-trip. There must be no synchronous computation that scales with request volume or identifier count.

**Fail-open behavior must be explicit and logged.** Every request that bypasses rate limiting due to a Redis failure must emit `ratelimit.failopen.request` and log at `WARN` level. Silent fail-open is not acceptable — operators must be able to see when the limiter is not functioning.

**Recovery from Redis outage must be automatic.** When Redis becomes available again, the rate limiter must resume normal operation without a process restart. The `ioredis` client handles reconnection; the rate limiter must not cache a "Redis is down" state in process memory.

---

### 6.3 Client Error Guidance

The 429 response is a contract with API clients. It must contain enough information for a well-behaved client to implement correct exponential backoff without guessing.

**Required client-facing information (all specified in §5):**
1. `Retry-After` header: authoritative seconds until the window resets. Clients must use this value, not a hardcoded backoff.
2. `X-RateLimit-Reset`: Unix timestamp of window reset, for clients that prefer absolute time.
3. `X-RateLimit-Limit`: The configured limit, so clients can self-throttle before hitting the limit.
4. `X-RateLimit-Window`: The window size, so clients can compute their sustainable request rate.
5. Response body `retryAfter` field: same value as header, for clients that parse JSON but not headers.

**What must not be in the 429 response:**
- The client's identifier (privacy and security concern).
- Internal Redis keys.
- Stack traces or internal error messages.
- A `Retry-After` value of 0 (this is a defect; minimum value is 1).

**Documentation requirement:** The implementing engineer must ensure that API documentation surfaced to external consumers includes the rate limit headers and their semantics. This document does not produce that documentation, but the implementation must make it possible.

---

### 6.4 Health Check

The rate limiter must expose its health state in a way that is consumable by load balancer health checks and Kubernetes readiness probes.

#### Liveness Check

**Endpoint (if standalone service):** `GET /healthz/live`
**Middleware integration:** Export a `isAlive()` function that returns `true` if the Node.js process is running and the middleware is initialized.

**Returns:** `200 OK`, body `{"status": "alive"}`
**Never returns a non-200 for liveness** unless the process should be killed and restarted. Redis unavailability does not affect liveness.

#### Readiness Check

**Endpoint (if standalone service):** `GET /healthz/ready`
**Middleware integration:** Export an async `isReady()` function.

**Logic:**
1. Attempt a Redis `PING` command with a 200ms timeout.
2. If `PING` succeeds: return `200 OK`, body `{"status": "ready", "redis": "ok"}`.
3. If `PING` fails or times out:
   - If `failOpen: true`: return `200 OK`, body `{"status": "ready", "redis": "degraded", "mode": "fail-open"}`. The service is ready to accept traffic; it will fail open.
   - If `failOpen: false`: return `503 Service Unavailable`, body `{"status": "not_ready", "redis": "unavailable"}`. The load balancer should stop sending traffic to this instance.

**The readiness check must not be on the hot path.** It must not run on every request. It must be a separate endpoint/function called by the health check infrastructure on its own schedule (typically every 10–30 seconds).

---

### 6.5 Alerting Policy

The following alert conditions must be configured before this system goes to production. Thresholds are specified as defaults; they must be tuned after observing baseline traffic.

| Alert Name | Condition | Severity | Action |
|---|---|---|---|
| `RateLimiterRedisDown` | `ratelimit.redis.error` rate > 5% of total requests for > 2 minutes | **P1 — Page immediately** | Redis is unavailable. All rate limiting is bypassed (fail-open) or all traffic is blocked (fail-closed). |
| `RateLimiterHighLatency` | `ratelimit.redis.latency_ms` p99 > 50ms for > 5 minutes | **P2 — Page** | Redis is slow. Every request is being delayed. Investigate Redis CPU, network, and key count. |
| `RateLimiterFailOpenTraffic` | `ratelimit.failopen.request` > 0 for > 1 minute | **P2 — Page** | Rate limiting is not functioning. Abuse is possible. |
| `RateLimiterHighRejectionRate` | `ratelimit.request.rejected` / `ratelimit.request.total` > 20% for > 5 minutes | **P3 — Ticket** | Either a legitimate traffic spike, a misconfigured limit, or an ongoing abuse pattern. Investigate before adjusting limits. |
| `RateLimiterIdentifierMissing` | `ratelimit.identifier.missing` > 0 for > 1 minute | **P3 — Ticket** | Identifier extraction is failing. Some requests are not being rate limited. Likely a proxy misconfiguration. |
| `RateLimiterScriptMiss` | `ratelimit.redis.script_miss` > 0 | **P3 — Ticket** | Redis was restarted or script cache was flushed. Script re-caching is automatic (F-07), but this warrants investigation. |

**Alert routing:** P1 alerts must page the on-call engineer immediately. P2 alerts must page within 5 minutes. P3 alerts must create a ticket and notify the team channel. Alert routing configuration is outside the scope of this document but must be established before go-live.

---

### 6.6 Load Test Specification

A load test must be executed and pass in a staging environment before any production deployment. The load test is not optional. The following scenarios must all be verified.

#### Required Test Scenarios

**LT-01: Steady-State Accuracy**
- Configuration: 100 requests per 60-second window, single identifier.
- Load: Send exactly 100 requests in 60 seconds at a uniform rate.
- Pass criterion: All 100 requests return 200. Request 101 (if sent within the same window) returns 429. Zero Redis errors.

**LT-02: Burst at Window Boundary**
- Configuration: 100 requests per 60-second window, single identifier.
- Load: Send 90 requests in the last 5 seconds of a window, then 90 requests in the first 5 seconds of the next window.
- Pass criterion: Total allowed requests must not exceed 110 (the ~10% approximation error bound). Document the actual observed overage.

**LT-03: Multi-Identifier Isolation**
- Configuration: 100 requests per 60-second window.
- Load: 1,000 unique identifiers each sending 100 requests concurrently.
- Pass criterion: Each identifier is independently limited. No identifier's limit is affected by another's traffic. Zero cross-contamination.

**LT-04: Redis Failure — Fail-Open**
- Configuration: `failOpen: true`.
- Load: 500 requests/second. Kill Redis mid-test. Restore Redis after 30 seconds.
- Pass criterion: Zero 429s during Redis outage. `ratelimit.failopen.request` counter increments during outage. Normal rate limiting resumes within 5 seconds of Redis restoration. Zero process crashes.

**LT-05: Redis Failure — Fail-Closed**
- Configuration: `failOpen: false`.
- Load: 500 requests/second. Kill Redis mid-test. Restore Redis after 30 seconds.
- Pass criterion: All requests during Redis outage return 503 with `Retry-After` header. Normal rate limiting resumes within 5 seconds of Redis restoration. Zero process crashes.

**LT-06: Sustained High Concurrency**
- Configuration: 1,000 requests per 60-second window, 10,000 unique identifiers.
- Load: 5,000 requests/second for 5 minutes.
- Pass criterion: `ratelimit.redis.latency_ms` p99 remains below 20ms. Node.js event loop lag remains below 10ms. Zero unhandled promise rejections. Redis memory usage matches estimate from §3.

**LT-07: Lua Script Eviction Recovery**
- Configuration: Any.
- Load: 100 requests/second. Execute `SCRIPT FLUSH` on Redis mid-test.
- Pass criterion: Zero 500 errors. `ratelimit.redis.script_miss` counter increments. Rate limiting continues correctly after script re-cache.

#### Load Test Infrastructure Requirements

- Staging Redis must be the same version and configuration as production Redis.
- Load generator must run on a separate host from the application under test.
- All metrics must be captured during the test and retained for comparison against future test runs.
- Test results must be documented and attached to the deployment record.

---

### 6.7 Incident Runbook Outline

This runbook is for the on-call engineer who is paged because the rate limiter is misbehaving. It covers the three most likely incident patterns.

---

#### Incident