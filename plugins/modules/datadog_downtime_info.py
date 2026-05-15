#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Steve Fulmer
# Apache-2.0 (see LICENSE)
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module: datadog_downtime_info."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: datadog_downtime_info
short_description: Retrieve downtime information
description:
    - Retrieve details about downtimes.
    - This is a read-only module.
version_added: "1.0.0"
author:
    - Steve Fulmer (@stevefulme1)
options:
    host:
        description: API host address.
        type: str
        required: true
    username:
        description: Authentication username.
        type: str
    password:
        description: Authentication password.
        type: str
        no_log: true
    api_key:
        description: API key for authentication.
        type: str
        no_log: true
    validate_certs:
        description: Whether to validate SSL certificates.
        type: bool
        default: true

    downtime_id:
        description: The downtime id.
        type: str
"""

EXAMPLES = r"""
- name: List all downtimes
  stevefulme1.datadog.datadog_downtime_info:
  register: result

- name: Get a specific downtime
  stevefulme1.datadog.datadog_downtime_info:
    downtime_id: "example-id"
  register: result
"""

RETURN = r"""
downtimes:
    description: List of downtime details.
    returned: always
    type: list
    elements: dict
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
            downtime_id=dict(type="str"),
            name=dict(type="str"),
            host=dict(type="str", required=True),
            username=dict(type="str"),
            password=dict(type="str", no_log=True),
            api_key=dict(type="str", no_log=True),
            validate_certs=dict(type="bool", default=True),
        ),
        supports_check_mode=True,
    )

    if not HAS_CLIENT:
        module.fail_json(msg="Required Python libraries not found.")

    client = ApiClient(module)
    resource_id = module.params.get("downtime_id")

    if resource_id:
        result = client.get("downtime", resource_id)
        resources = [result] if result else []
    else:
        resources = client.list("downtime", module.params)

    module.exit_json(changed=False, downtimes=resources)


if __name__ == "__main__":
    main()
