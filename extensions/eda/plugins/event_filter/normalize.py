"""Normalize Datadog webhook payloads into a flat event structure."""

DOCUMENTATION = r"""
---
event_filter: normalize
short_description: Flatten Datadog webhook payloads
description:
  - Normalizes nested Datadog monitor/event webhook payloads into a
    flat key-value structure suitable for EDA rule matching.
  - Extracts fields from alert, monitor, and event blocks.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
options:
  include_raw:
    description: Whether to include the original raw payload under a C(raw) key.
    type: bool
    default: false
"""

EXAMPLES = r"""
- stevefulme1.datadog.normalize:
    include_raw: false
"""


def main(event, include_raw=False):
    """Flatten a Datadog webhook payload."""
    if not isinstance(event, dict):
        return event

    payload = event.get("payload", event)
    result = {}

    for key in ("id", "title", "body", "priority", "alert_type",
                "alert_id", "date_happened", "org_id", "host",
                "event_type", "alert_status", "alert_metric",
                "alert_query", "alert_scope", "alert_transition",
                "monitor_id", "monitor_name", "tags"):
        if key in payload:
            result[key] = payload[key]

    # Flatten tags list to dict
    tags = payload.get("tags", [])
    if isinstance(tags, list):
        for tag in tags:
            if ":" in str(tag):
                k, v = str(tag).split(":", 1)
                result["tag_" + k] = v

    if include_raw:
        result["raw"] = event

    for key in ("meta", "source"):
        if key in event:
            result[key] = event[key]

    return result
