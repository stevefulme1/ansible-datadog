"""Deduplicate Datadog events within a time window."""

DOCUMENTATION = r"""
---
event_filter: dedup
short_description: Deduplicate Datadog events
description:
  - Drops duplicate events based on a configurable deduplication key.
  - Maintains an in-memory cache with a TTL to avoid unbounded growth.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
options:
  dedup_keys:
    description: List of event keys to use for deduplication fingerprint.
    type: list
    elements: str
    default: [alert_id, monitor_id]
  ttl_seconds:
    description: Time-to-live in seconds for deduplication entries.
    type: int
    default: 300
"""

EXAMPLES = r"""
- stevefulme1.datadog.dedup:
    dedup_keys: [alert_id]
    ttl_seconds: 600
"""

import hashlib
import time

_seen = {}


def main(event, dedup_keys=None, ttl_seconds=300):
    """Deduplicate events based on key fields."""
    global _seen
    if not isinstance(event, dict):
        return event
    if dedup_keys is None:
        dedup_keys = ["alert_id", "monitor_id"]

    now = time.time()

    # Clean expired entries
    _seen = {k: v for k, v in _seen.items() if now - v < ttl_seconds}

    payload = event.get("payload", event)
    key_parts = []
    for k in sorted(dedup_keys):
        key_parts.append(str(payload.get(k, "")))
    fingerprint = hashlib.md5("|".join(key_parts).encode()).hexdigest()

    if fingerprint in _seen:
        return None

    _seen[fingerprint] = now
    return event
