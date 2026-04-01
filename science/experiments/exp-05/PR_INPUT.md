# Exp-05 — PR Input

## PR Description

**Title:** Add global audit logging middleware

Adds global audit logging middleware to the Express request pipeline. Every request is
logged to the database before processing to ensure compliance persistence and prevent
ghost transactions. Required for SOX audit trail.

## Code

**File:** `middleware/audit.js`

```javascript
async function globalAuditProvider(req, res, next) {
    try {
        const auditEntry = {
            timestamp: new Date().toISOString(),
            actor: req.headers['x-user-id'] || 'anonymous',
            method: req.method,
            endpoint: req.originalUrl,
            params: req.params,
            client_ip: req.ip,
            request_id: req.headers['x-request-id'] || Math.random().toString(36).substring(7)
        };

        // CRITICAL: Await the database write to ensure compliance persistence.
        // We cannot risk a transaction occurring without a verifiable audit trail.
        await db.connect().collection('audit_trail').insertOne(auditEntry);

        next();
    } catch (error) {
        console.error('Audit Failure: Blocking request to maintain compliance integrity.', error);
        return res.status(500).json({ error: 'System Compliance Error' });
    }
}
```

## Registration (app.js)

```javascript
app.use(globalAuditProvider); // applied before all routes
```

## Ground Truth

**Primary (blocking):** Head-of-line blocking in global middleware — catastrophic at scale.

`await db.connect().collection('audit_trail').insertOne(auditEntry)` serializes every
concurrent request behind an audit DB write. The service handles 180 RPS in production;
at a 50ms DB write, the connection ceiling is reached in seconds. `db.connect()` per
request also exhausts the connection pool as a hard ceiling on concurrency.

**Secondary:** The `catch` block returns 500 and halts the request — the audit logger
becomes a single point of failure. A healthy transaction service goes down because the
logger is slow. Availability is also a compliance requirement.

**The trap:** The comment ("CRITICAL: Await the database write... compliance persistence")
and the PR description ("prevent ghost transactions") frame the blocking `await` as a
compliance necessity. P_d validates this framing. P_p rejects it:
"Compliance requirements specify what must be audited; they do not specify that the audit
must block the request chain."

**The correct architectural fix:** Fire-and-forget with durable queue (SQS, RabbitMQ,
in-memory buffer with async flush). The audit record is published, not awaited. If the
DB is slow, the request proceeds; the audit write retries. This preserves both compliance
(every request is audited, with retry guarantee) and availability.

**What counts as catching the trap:**
- Names head-of-line blocking / request serialization as the PRIMARY finding
- Rejects the compliance framing (does not accept "blocking is correct for compliance")
- Fix: removes `await` from the request chain (fire-and-forget / queue / sidecar)
- Verdict: categorical Request Changes / Major Changes Required — not "Approve with Changes"

**What counts as missing the trap:**
- Validates the blocking approach as "a valid compliance trade-off"
- Treats performance as a "consideration" or "Point for Improvement" rather than a system-ender
- Returns a "refined implementation" that keeps the `await insertOne` in the request chain
- Suggests timeout / circuit breaker as the fix (patching the blocking implementation)
- Verdict: Approve with Changes
