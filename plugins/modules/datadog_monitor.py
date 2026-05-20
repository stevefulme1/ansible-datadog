#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Steve Fulmer
# Apache-2.0 (see LICENSE)
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module: datadog_monitor."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: datadog_monitor
short_description: Manage Datadog monitors
description:
    - Create, update, and delete Datadog monitors using the Monitors API v1.
    - "API reference: GET/POST/PUT/DELETE /api/v1/monitor/{id}"
    - Supports full idempotency and check_mode with diff.
version_added: "1.0.0"
author:
    - Steve Fulmer (@stevefulme1)
options:
    state:
        description: Desired state of the monitor.
        type: str
        default: present
        choices: [present, absent]
    monitor_id:
        description:
            - The ID of the monitor.
            - Required when O(state=absent).
        type: str
    name:
        description: Name of the monitor.
        type: str
    monitor_type:
        description: The type of monitor (e.g. metric alert, service check).
        type: str
    query:
        description: The monitor query.
        type: str
    message:
        description: Notification message body.
        type: str
    tags:
        description: Tags to associate with the monitor.
        type: list
        elements: str
    priority:
        description: Monitor priority (1-5).
        type: int
    options:
        description: Monitor options (thresholds, notify settings, etc.).
        type: dict
    host:
        description: Datadog API host (e.g. api.datadoghq.com).
        type: str
        required: true
    api_key:
        description: Datadog API key.
        type: str
        no_log: true
    app_key:
        description: Datadog application key.
        type: str
        no_log: true
    validate_certs:
        description: Whether to validate SSL certificates.
        type: bool
        default: true
"""

EXAMPLES = r"""
- name: Create a metric monitor
  stevefulme1.datadog.datadog_monitor:
    host: api.datadoghq.com
    api_key: "{{ datadog_api_key }}"
    app_key: "{{ datadog_app_key }}"
    state: present
    name: High CPU on web servers
    monitor_type: metric alert
    query: "avg(last_5m):avg:system.cpu.user{role:web} > 90"
    message: "CPU is above 90% on {{host.name}}"
    tags:
      - env:production
      - team:platform

- name: Delete a monitor by ID
  stevefulme1.datadog.datadog_monitor:
    host: api.datadoghq.com
    api_key: "{{ datadog_api_key }}"
    app_key: "{{ datadog_app_key }}"
    monitor_id: "12345"
    state: absent
"""

RETURN = r"""
monitor:
    description: The monitor resource returned by the Datadog API.
    returned: on success
    type: dict
    sample:
        id: 12345
        name: High CPU on web servers
        type: metric alert
diff:
    description: Before/after state for check_mode and changes.
    returned: when changed
    type: dict
"""

from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.stevefulme1.datadog.plugins.module_utils.api_client import ApiClient
    HAS_CLIENT = True
except ImportError:
    HAS_CLIENT = False

# Fields that define desired state (compared for idempotency)
COMPARE_FIELDS = ("name", "monitor_type", "query", "message", "tags", "priority", "options")


def get_current_state(client, module):
    """Fetch current monitor state. Returns None if not found (404)."""
    resource_id = module.params.get("monitor_id")
    if resource_id:
        return client.get("monitor", resource_id)
    name = module.params.get("name")
    if name:
        return client.find_by_name("monitor", name)
    return None


def build_payload(module):
    """Build the API payload from module params."""
    payload = {}
    field_map = {
        "name": "name",
        "monitor_type": "type",
        "query": "query",
        "message": "message",
        "tags": "tags",
        "priority": "priority",
        "options": "options",
    }
    for param, api_field in field_map.items():
        value = module.params.get(param)
        if value is not None:
            payload[api_field] = value
    return payload


def needs_update(current, desired):
    """Compare current API state against desired params. Returns True if different."""
    field_map = {
        "name": "name",
        "type": "monitor_type",
        "query": "query",
        "message": "message",
        "tags": "tags",
        "priority": "priority",
        "options": "options",
    }
    for api_field, param in field_map.items():
        if param not in ("name", "monitor_type", "query", "message", "tags", "priority", "options"):
            continue
        desired_val = desired.get(api_field)
        if desired_val is None:
            continue
        current_val = current.get(api_field)
        if isinstance(desired_val, list) and isinstance(current_val, list):
            if sorted(desired_val) != sorted(current_val):
                return True
        elif current_val != desired_val:
            return True
    return False


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type="str", default="present", choices=["present", "absent"]),
            monitor_id=dict(type="str"),
            name=dict(type="str"),
            monitor_type=dict(type="str"),
            query=dict(type="str"),
            message=dict(type="str"),
            tags=dict(type="list", elements="str"),
            priority=dict(type="int"),
            options=dict(type="dict"),
            host=dict(type="str", required=True),
            api_key=dict(type="str", no_log=True),
            app_key=dict(type="str", no_log=True),
            validate_certs=dict(type="bool", default=True),
        ),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("monitor_id",)),
            ("state", "present", ("name",)),
        ],
    )

    if not HAS_CLIENT:
        module.fail_json(msg="Required library 'requests' is not installed.")

    client = ApiClient(module)
    state = module.params["state"]

    current = get_current_state(client, module)
    payload = build_payload(module)

    if state == "present":
        if current:
            # Resource exists -- check if update is needed
            if needs_update(current, payload):
                resource_id = current.get("id", module.params.get("monitor_id", ""))
                diff = {"before": current, "after": payload}
                if module.check_mode:
                    module.exit_json(changed=True, monitor=current, diff=diff)
                result = client.update("monitor", resource_id, payload)
                module.exit_json(changed=True, monitor=result, diff=diff)
            else:
                # No changes needed -- idempotent
                module.exit_json(changed=False, monitor=current)
        else:
            # Resource does not exist -- create
            if module.check_mode:
                module.exit_json(changed=True, diff={"before": {}, "after": payload})
            result = client.create("monitor", payload)
            module.exit_json(changed=True, monitor=result,
                             diff={"before": {}, "after": payload})
    else:
        # state == absent
        if not current:
            module.exit_json(changed=False)
        if module.check_mode:
            module.exit_json(changed=True, diff={"before": current, "after": {}})
        client.delete("monitor", module.params["monitor_id"])
        module.exit_json(changed=True, diff={"before": current, "after": {}})


if __name__ == "__main__":
    main()
