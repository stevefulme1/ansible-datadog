#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Steve Fulmer
# Apache-2.0 (see LICENSE)

"""Ansible module: datadog_synthetic_info."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: datadog_synthetic_info
short_description: Retrieve synthetic information
description:
    - Retrieve details about synthetics.
    - This is a read-only module.
version_added: "1.0.0"
author:
    - Steve Fulmer (@stevefulme1)
options:
    public_id:
        description: ID of a specific synthetic to retrieve.
        type: str
    name:
        description: Filter by name.
        type: str
"""

EXAMPLES = r"""
- name: List all synthetics
  stevefulme1.datadog.datadog_synthetic_info:
  register: result

- name: Get a specific synthetic
  stevefulme1.datadog.datadog_synthetic_info:
    public_id: "example-id"
  register: result
"""

RETURN = r"""
synthetics:
    description: List of synthetic details.
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
            public_id=dict(type="str"),
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
    resource_id = module.params.get("public_id")

    if resource_id:
        result = client.get("synthetic", resource_id)
        resources = [result] if result else []
    else:
        resources = client.list("synthetic", module.params)

    module.exit_json(changed=False, synthetics=resources)


if __name__ == "__main__":
    main()
