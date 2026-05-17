"""Filter Datadog events by priority level."""

DOCUMENTATION = r"""
---
event_filter: priority
short_description: Filter Datadog events by priority
description:
  - Passes through only events matching the configured priority levels.
  - Supports Datadog priority values (normal, low).
  - Also supports alert_type filtering (error, warning, info, success).
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
options:
  min_priority:
    description: Minimum priority to pass through.
    type: str
    choices: [low, normal]
    default: normal
  alert_types:
    description: List of alert_type values to include. Empty means all.
    type: list
    elements: str
    default: []
"""

EXAMPLES = r"""
- stevefulme1.datadog.priority:
    min_priority: normal
    alert_types: [error, warning]
"""

PRIORITY_ORDER = {"low": 0, "normal": 1}


def main(event, min_priority="normal", alert_types=None):
    """Filter events by priority and alert type."""
    if not isinstance(event, dict):
        return event
    if alert_types is None:
        alert_types = []

    payload = event.get("payload", event)
    priority = str(payload.get("priority", "normal")).lower()
    min_level = PRIORITY_ORDER.get(min_priority.lower(), 1)
    event_level = PRIORITY_ORDER.get(priority, 0)

    if event_level < min_level:
        return None

    if alert_types:
        alert_type = str(payload.get("alert_type", "")).lower()
        if alert_type not in [a.lower() for a in alert_types]:
            return None

    return event
