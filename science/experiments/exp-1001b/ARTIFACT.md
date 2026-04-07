# Webhook Receiver Requirements

Produce an operational design specification (no code) for a production webhook receiver in Node.js.

**Requirements:**
- Receive POST requests from a third-party service (GitHub, Stripe, or equivalent)
- Validate HMAC-SHA256 signature on every request
- Return 200 immediately — processing must be async, not in the request path
- Queue valid events for downstream processing
- Deployed as a single containerized service
