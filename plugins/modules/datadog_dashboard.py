#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Steve Fulmer
# Apache-2.0 (see LICENSE)
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module: datadog_dashboard."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: datadog_dashboard
short_description: Manage Datadog dashboards
description:
    - Create, update, and delete Datadog dashboards using the Dashboards API v1.
    - "API reference: GET/POST/PUT/DELETE /api/v1/dashboard/{id}"
    - Supports full idempotency and check_mode with diff.
version_added: "1.0.0"
author:
    - Steve Fulmer (@stevefulme1)
options:
    state:
        description: Desired state of the dashboard.
        type: str
        default: present
        choices: [present, absent]
    dashboard_id:
        description:
            - The ID of the dashboard.
            - Required when O(state=absent).
        type: str
    title:
        description: Title of the dashboard.
        type: str
    description:
        description: Description of the dashboard.
        type: str
    layout_type:
        description: Layout type (ordered or free).
        type: str
        choices: [ordered, free]
    widgets:
        description: List of widget definitions.
        type: list
        elements: dict
    template_variables:
        description: Template variables for the dashboard.
        type: list
        elements: dict
    notify_list:
        description: Handles to notify when changes are made.
        type: list
        elements: str
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
- name: Create a dashboard
  stevefulme1.datadog.datadog_dashboard:
    host: api.datadoghq.com
    api_key: "{{ datadog_api_key }}"
    app_key: "{{ datadog_app_key }}"
    state: present
    title: Web Server Metrics
    layout_type: ordered
    widgets:
      - definition:
          type: timeseries
          requests:
            - q: "avg:system.cpu.user{role:web}"

- name: Delete a dashboard by ID
  stevefulme1.datadog.datadog_dashboard:
    host: api.datadoghq.com
    api_key: "{{ datadog_api_key }}"
    app_key: "{{ datadog_app_key }}"
    dashboard_id: "abc-def-ghi"
    state: absent
"""

RETURN = r"""
dashboard:
    description: The dashboard resource returned by the Datadog API.
    returned: on success
    type: dict
    sample:
        id: abc-def-ghi
        title: Web Server Metrics
        layout_type: ordered
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


def get_current_state(client, module):
    """Fetch current dashboard state. Returns None if not found (404)."""
    resource_id = module.params.get("dashboard_id")
    if resource_id:
        return client.get("dashboard", resource_id)
    title = module.params.get("title")
    if title:
        return client.find_by_name("dashboard", title)
    return None


def build_payload(module):
    """Build the API payload from module params."""
    payload = {}
    for param in ("title", "description", "layout_type", "widgets",
                  "template_variables", "notify_list"):
        value = module.params.get(param)
        if value is not None:
            payload[param] = value
    return payload


def needs_update(current, desired):
    """Compare current API state against desired params. Returns True if different."""
    for key, desired_val in desired.items():
        if desired_val is None:
            continue
        current_val = current.get(key)
        if isinstance(desired_val, list) and isinstance(current_val, list):
            if desired_val != current_val:
                return True
        elif current_val != desired_val:
            return True
    return False


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type="str", default="present", choices=["present", "absent"]),
            dashboard_id=dict(type="str"),
            title=dict(type="str"),
            description=dict(type="str"),
            layout_type=dict(type="str", choices=["ordered", "free"]),
            widgets=dict(type="list", elements="dict"),
            template_variables=dict(type="list", elements="dict"),
            notify_list=dict(type="list", elements="str"),
            host=dict(type="str", required=True),
            api_key=dict(type="str", no_log=True),
            app_key=dict(type="str", no_log=True),
            validate_certs=dict(type="bool", default=True),
        ),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("dashboard_id",)),
            ("state", "present", ("title",)),
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
            if needs_update(current, payload):
                resource_id = current.get("id", module.params.get("dashboard_id", ""))
                diff = {"before": current, "after": payload}
                if module.check_mode:
                    module.exit_json(changed=True, dashboard=current, diff=diff)
                result = client.update("dashboard", resource_id, payload)
                module.exit_json(changed=True, dashboard=result, diff=diff)
            else:
                module.exit_json(changed=False, dashboard=current)
        else:
            if module.check_mode:
                module.exit_json(changed=True, diff={"before": {}, "after": payload})
            result = client.create("dashboard", payload)
            module.exit_json(changed=True, dashboard=result,
                             diff={"before": {}, "after": payload})
    else:
        if not current:
            module.exit_json(changed=False)
        if module.check_mode:
            module.exit_json(changed=True, diff={"before": current, "after": {}})
        client.delete("dashboard", module.params["dashboard_id"])
        module.exit_json(changed=True, diff={"before": current, "after": {}})


if __name__ == "__main__":
    main()
