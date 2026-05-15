#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Steve Fulmer
# Apache-2.0 (see LICENSE)

"""Ansible module: datadog_monitor."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: datadog_monitor
short_description: Manage Datadog monitors (metric, anomaly, outlier, etc.)
description:
    - Manage Datadog monitors (metric, anomaly, outlier, etc.) in Datadog.
    - Supports create, update, and delete operations.
version_added: "1.0.0"
author:
    - Steve Fulmer (@stevefulme1)
options:
    state:
        description: Desired state of the resource.
        type: str
        default: present
        choices: [present, absent]
    monitor_id:
        description: Unique identifier of the monitor.
        type: str
    name:
        description: Display name of the monitor.
        type: str
"""

EXAMPLES = r"""
- name: Create a monitor
  stevefulme1.datadog.datadog_monitor:
    name: my-monitor
    state: present

- name: Delete a monitor
  stevefulme1.datadog.datadog_monitor:
    monitor_id: "example-id"
    state: absent
"""

RETURN = r"""
monitor:
    description: Resource details.
    returned: on success
    type: dict
"""

from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.stevefulme1.datadog.plugins.module_utils.api_client import ApiClient
    HAS_CLIENT = True
except ImportError:
    HAS_CLIENT = False


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type="str", default="present", choices=["present", "absent"]),
            monitor_id=dict(type="str"),
            name=dict(type="str"),
            host=dict(type="str", required=True),
            username=dict(type="str"),
            password=dict(type="str", no_log=True),
            api_key=dict(type="str", no_log=True),
            validate_certs=dict(type="bool", default=True),
        ),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("monitor_id",)),
        ],
    )

    if not HAS_CLIENT:
        module.fail_json(msg="Required Python libraries not found.")

    client = ApiClient(module)
    state = module.params["state"]
    resource_id = module.params.get("monitor_id")

    if state == "present":
        if resource_id:
            result = client.update("monitor", resource_id, module.params)
        else:
            if module.check_mode:
                module.exit_json(changed=True)
            result = client.create("monitor", module.params)
        module.exit_json(changed=True, monitor=result)
    else:
        if module.check_mode:
            module.exit_json(changed=True)
        client.delete("monitor", resource_id)
        module.exit_json(changed=True)


if __name__ == "__main__":
    main()
