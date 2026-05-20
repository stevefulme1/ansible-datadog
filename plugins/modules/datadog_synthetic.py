#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Steve Fulmer
# Apache-2.0 (see LICENSE)
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module: datadog_synthetic."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: datadog_synthetic
short_description: Manage Datadog synthetic tests
description:
    - Create, update, and delete Datadog synthetic API/browser tests using the Synthetics API v1.
    - "API reference: GET/POST/PUT/DELETE /api/v1/synthetics/tests/{public_id}"
    - Supports full idempotency and check_mode with diff.
version_added: "1.0.0"
author:
    - Steve Fulmer (@stevefulme1)
options:
    state:
        description: Desired state of the synthetic test.
        type: str
        default: present
        choices: [present, absent]
    public_id:
        description:
            - The public ID of the synthetic test.
            - Required when O(state=absent).
        type: str
    name:
        description: Name of the synthetic test.
        type: str
    test_type:
        description: Type of synthetic test (api or browser).
        type: str
        choices: [api, browser]
    config:
        description: Test configuration (assertions, request definition, etc.).
        type: dict
    locations:
        description: List of locations to run the test from.
        type: list
        elements: str
    message:
        description: Notification message.
        type: str
    tags:
        description: Tags to associate with the test.
        type: list
        elements: str
    status:
        description: Test status (live or paused).
        type: str
        choices: [live, paused]
    options_config:
        description: Test options (frequency, retry, etc.).
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
- name: Create an API synthetic test
  stevefulme1.datadog.datadog_synthetic:
    host: api.datadoghq.com
    api_key: "{{ datadog_api_key }}"
    app_key: "{{ datadog_app_key }}"
    state: present
    name: API Health Check
    test_type: api
    config:
      assertions:
        - type: statusCode
          operator: is
          target: 200
      request:
        method: GET
        url: "https://example.com/health"
    locations:
      - aws:us-east-1
    message: "Health check failed on example.com"
    tags:
      - env:production

- name: Delete a synthetic test
  stevefulme1.datadog.datadog_synthetic:
    host: api.datadoghq.com
    api_key: "{{ datadog_api_key }}"
    app_key: "{{ datadog_app_key }}"
    public_id: "abc-123-def"
    state: absent
"""

RETURN = r"""
synthetic:
    description: The synthetic test resource returned by the Datadog API.
    returned: on success
    type: dict
    sample:
        public_id: abc-123-def
        name: API Health Check
        type: api
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
    """Fetch current synthetic test state. Returns None if not found (404)."""
    resource_id = module.params.get("public_id")
    if resource_id:
        return client.get("synthetic", resource_id)
    name = module.params.get("name")
    if name:
        return client.find_by_name("synthetic", name)
    return None


def build_payload(module):
    """Build the API payload from module params."""
    payload = {}
    field_map = {
        "name": "name",
        "test_type": "type",
        "config": "config",
        "locations": "locations",
        "message": "message",
        "tags": "tags",
        "status": "status",
        "options_config": "options",
    }
    for param, api_field in field_map.items():
        value = module.params.get(param)
        if value is not None:
            payload[api_field] = value
    return payload


def needs_update(current, desired):
    """Compare current API state against desired params. Returns True if different."""
    for key, desired_val in desired.items():
        if desired_val is None:
            continue
        current_val = current.get(key)
        if isinstance(desired_val, list) and isinstance(current_val, list):
            if sorted(str(x) for x in desired_val) != sorted(str(x) for x in current_val):
                return True
        elif isinstance(desired_val, dict) and isinstance(current_val, dict):
            if desired_val != current_val:
                return True
        elif current_val != desired_val:
            return True
    return False


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type="str", default="present", choices=["present", "absent"]),
            public_id=dict(type="str"),
            name=dict(type="str"),
            test_type=dict(type="str", choices=["api", "browser"]),
            config=dict(type="dict"),
            locations=dict(type="list", elements="str"),
            message=dict(type="str"),
            tags=dict(type="list", elements="str"),
            status=dict(type="str", choices=["live", "paused"]),
            options_config=dict(type="dict"),
            host=dict(type="str", required=True),
            api_key=dict(type="str", no_log=True),
            app_key=dict(type="str", no_log=True),
            validate_certs=dict(type="bool", default=True),
        ),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("public_id",)),
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
            if needs_update(current, payload):
                resource_id = current.get("public_id", module.params.get("public_id", ""))
                diff = {"before": current, "after": payload}
                if module.check_mode:
                    module.exit_json(changed=True, synthetic=current, diff=diff)
                result = client.update("synthetic", resource_id, payload)
                module.exit_json(changed=True, synthetic=result, diff=diff)
            else:
                module.exit_json(changed=False, synthetic=current)
        else:
            if module.check_mode:
                module.exit_json(changed=True, diff={"before": {}, "after": payload})
            result = client.create("synthetic", payload)
            module.exit_json(changed=True, synthetic=result,
                             diff={"before": {}, "after": payload})
    else:
        if not current:
            module.exit_json(changed=False)
        if module.check_mode:
            module.exit_json(changed=True, diff={"before": current, "after": {}})
        client.delete("synthetic", module.params["public_id"])
        module.exit_json(changed=True, diff={"before": current, "after": {}})


if __name__ == "__main__":
    main()
