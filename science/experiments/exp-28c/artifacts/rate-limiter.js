/**
 * Rate Limiter — Node.js / Redis
 *
 * Sliding window algorithm backed by Redis. Supports per-key limiting
 * (by IP, user ID, or API key) via the keyBy option.
 */

const redis = require('ioredis');
const { v4: uuidv4 } = require('uuid');

// Lua script for atomic sliding window check-and-add.
// Removes expired entries, counts current window, adds if under limit.
const SLIDING_WINDOW_SCRIPT = `
local key = KEYS[1]
local window_ms = tonumber(ARGV[1])
local limit = tonumber(ARGV[2])
local now = tonumber(ARGV[3])
local request_id = ARGV[4]

redis.call('ZREMRANGEBYSCORE', key, 0, now - window_ms)
local count = redis.call('ZCARD', key)

if count < limit then
  redis.call('ZADD', key, now, request_id)
  redis.call('PEXPIRE', key, window_ms)
  return {1, count + 1}
else
  return {0, count}
end
`;


// ─── RateLimiter ─────────────────────────────────────────────────────────────

class RateLimiter {
  /**
   * @param {object} opts
   * @param {number}  opts.windowMs      - Window size in milliseconds
   * @param {number}  opts.limit         - Max requests per window
   * @param {string}  [opts.keyPrefix]   - Redis key namespace (default: 'rl')
   * @param {object}  opts.redisClient   - ioredis client instance
   */
  constructor({ windowMs, limit, keyPrefix = 'rl', redisClient }) {
    this.windowMs = windowMs;
    this.limit = limit;
    this.keyPrefix = keyPrefix;
    this.redis = redisClient;
    this._scriptSha = null;
  }

  async _loadScript() {
    this._scriptSha = await this.redis.script('LOAD', SLIDING_WINDOW_SCRIPT);
  }

  /**
   * Check whether a request identified by `identifier` is within the limit.
   *
   * @param  {string} identifier - Caller identifier (IP, user ID, API key, etc.)
   * @returns {{ allowed: boolean, count: number, remaining: number, limit: number, resetAt: string }}
   */
  async check(identifier) {
    const key = `${this.keyPrefix}:${identifier}`;
    const now = Date.now();
    const requestId = uuidv4();

    if (!this._scriptSha) {
      await this._loadScript();
    }

    let result;
    try {
      result = await this.redis.evalsha(
        this._scriptSha, 1, key,
        String(this.windowMs), String(this.limit), String(now), requestId
      );
    } catch (err) {
      if (err.message && err.message.includes('NOSCRIPT')) {
        await this._loadScript();
        result = await this.redis.evalsha(
          this._scriptSha, 1, key,
          String(this.windowMs), String(this.limit), String(now), requestId
        );
      } else {
        throw err;
      }
    }

    const [allowed, count] = result;

    return {
      allowed: allowed === 1,
      count,
      remaining: Math.max(0, this.limit - count),
      limit: this.limit,
      resetAt: new Date(now + this.windowMs).toISOString(),
    };
  }
}


// ─── Middleware ───────────────────────────────────────────────────────────────

/**
 * Express middleware factory.
 *
 * @param {RateLimiter} rateLimiter
 * @param {object}      [options]
 * @param {function}    [options.keyBy]  - (req) => string; defaults to req.ip
 * @returns Express middleware
 */
function createRateLimitMiddleware(rateLimiter, options = {}) {
  const getIdentifier = options.keyBy || (req => req.ip);

  return async function rateLimitMiddleware(req, res, next) {
    const identifier = getIdentifier(req);
    const result = await rateLimiter.check(identifier);

    if (!result.allowed) {
      return res.status(429).json({
        error: 'Too Many Requests',
        retryAfter: Math.ceil(rateLimiter.windowMs / 1000),
      });
    }

    next();
  };
}


// ─── Bootstrap ───────────────────────────────────────────────────────────────

const express = require('express');

const redisClient = new redis({
  host: process.env.REDIS_HOST || 'localhost',
  port: Number(process.env.REDIS_PORT) || 6379,
});

const limiter = new RateLimiter({
  windowMs: 60 * 1000,   // 1 minute
  limit: 100,
  keyPrefix: 'api:rl',
  redisClient,
});

const app = express();

app.use(express.json());

// Apply rate limiting to all API routes, keyed by authenticated user or IP.
app.use('/api', createRateLimitMiddleware(limiter, {
  keyBy: req => req.headers['x-user-id'] || req.ip,
}));

app.get('/api/data', (req, res) => {
  res.json({ data: 'example response' });
});

app.listen(3000, () => {
  console.log('Server listening on port 3000');
});

module.exports = { RateLimiter, createRateLimitMiddleware };
