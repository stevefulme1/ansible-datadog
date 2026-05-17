#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Steve Fulmer
# Apache-2.0 (see LICENSE)
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""datadog_widget module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: datadog_widget
short_description: Manage Datadog dashboard widgets
description:
    - Manage Datadog dashboard widgets.
version_added: "1.0.0"
author:
    - Steve Fulmer (@stevefulme1)
options:
    state:
        description: Desired state of the resource.
        type: str
        default: present
        choices: [present, absent]
    host:
        description: API host address.
        type: str
        required: true
    widget_id:
        description: Unique identifier.
        type: str
    name:
        description: Display name.
        type: str
    username:
        description: Authentication username.
        type: str
    password:
        description: Authentication password.
        type: str
    api_key:
        description: API key for authentication.
        type: str
    validate_certs:
        description: Validate SSL certificates.
        type: bool
        default: true
"""

EXAMPLES = r"""
- name: Create
  stevefulme1.datadog.datadog_widget:
    host: api.example.com
    name: my-resource
    state: present

- name: Delete
  stevefulme1.datadog.datadog_widget:
    host: api.example.com
    widget_id: "example-id"
    state: absent
"""

RETURN = r"""
widget:
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
            widget_id=dict(type="str"),
            name=dict(type="str"),
            host=dict(type="str", required=True),
            username=dict(type="str"),
            password=dict(type="str", no_log=True),
            api_key=dict(type="str", no_log=True),
            validate_certs=dict(type="bool", default=True),
        ),
        supports_check_mode=True,
        required_if=[("state", "absent", ("widget_id",))],
    )

    if not HAS_CLIENT:
        module.fail_json(msg="Required Python libraries not found.")

    client = ApiClient(module)
    state = module.params["state"]
    resource_id = module.params.get("widget_id")

    if state == "present":
        existing = None
        if resource_id:
            existing = client.get("widget", resource_id)
        elif module.params.get("name"):
            candidates = client.list("widget", {{"name": module.params["name"]}})
            if candidates:
                existing = candidates[0]

        if existing:
            if module.check_mode:
                module.exit_json(changed=False, widget=existing)
            result = client.update("widget", resource_id or existing.get("id", ""), module.params)
            module.exit_json(changed=True, widget=result)
        else:
            if module.check_mode:
                module.exit_json(changed=True)
            result = client.create("widget", module.params)
            module.exit_json(changed=True, widget=result)
    else:
        existing = None
        if resource_id:
            existing = client.get("widget", resource_id)
        if not existing:
            module.exit_json(changed=False)
        if module.check_mode:
            module.exit_json(changed=True)
        client.delete("widget", resource_id)
        module.exit_json(changed=True)


if __name__ == "__main__":
    main()
