#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Auto-generated from Datadog API spec
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from ansible_collections.stevefulme1.datadog.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)
from ansible.module_utils.basic import AnsibleModule

__metaclass__ = type

DOCUMENTATION = r"""
---
module: synthetic_test_info
short_description: Retrieve information about synthetic_test resources
version_added: "1.0.0"
description:
  - Retrieve a single synthetic_test by its identifier, or list all synthetic_test resources.
  - This module always reports C(changed=False).
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  monitor_id:
    description:
      - The unique identifier of the synthetic_test to retrieve.
      - When omitted, all synthetic_test resources are listed.
    type: str
    required: false

  name:
    description:
      - Filter results by name.
    type: str
    required: false

  page:
    description:
      - Page number for paginated results.
      - Only applies when listing resources.
    type: int
    required: false
  page_size:
    description:
      - Number of results per page.
      - Only applies when listing resources.
    type: int
    required: false
extends_documentation_fragment:
  - stevefulme1.datadog.auth
"""

EXAMPLES = r"""
- name: Get a specific synthetic_test
  stevefulme1.datadog.synthetic_test_info:
    monitor_id: "example_id"
  register: result

- name: List all synthetic_test resources
  stevefulme1.datadog.synthetic_test_info:
  register: result

- name: List synthetic_test resources filtered by name
  stevefulme1.datadog.synthetic_test_info:
    name: "my_synthetic_test"
  register: result

- name: List synthetic_test resources with pagination
  stevefulme1.datadog.synthetic_test_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
synthetic_tests:
  description: List of synthetic_test resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:

    config:
      description: >-
        Configuration object for a Synthetic test.
      type: dict

    creator:
      description: >-
        Object describing the creator of the shared element.
      type: dict

    locations:
      description: >-
        Array of locations used to run the test.
      type: list

    message:
      description: >-
        Notification message associated with the test.
      type: str

    monitor_id:
      description: >-
        The associated monitor ID.
      type: int

    name:
      description: >-
        Name of the test.
      type: str

    options:
      description: >-
        Object describing the extra options for a Synthetic test.
      type: dict

    public_id:
      description: >-
        The test public ID.
      type: str

    status:
      description: >-
        Define whether you want to start (live) or pause (paused) a Synthetic test.
      type: str

    subtype:
      description: >-
        The subtype of the Synthetic API test, http, ssl, tcp, dns, icmp, udp, websocket, grpc or multi.
      type: str

    tags:
      description: >-
        Array of tags attached to the test.
      type: list

    type:
      description: >-
        Type of the Synthetic test.
      type: str

"""


def fetch_single(client, identifier):
    """Retrieve a single synthetic_test by identifier."""

    # No single-resource GET endpoint; filter from list
    items = client.get("/api/v1/synthetics/tests")
    if isinstance(items, dict):
        items = items.get("results", items.get("data", items.get("items", [])))
    for item in items:
        if str(item.get("monitor_id")) == str(identifier):
            return item
    return None


def fetch_list(client, module):
    """List synthetic_test resources with optional filtering and pagination."""

    params = {}

    name_filter = module.params.get("name")
    if name_filter is not None:
        params["name"] = name_filter

    page = module.params.get("page")
    page_size = module.params.get("page_size")

    if page is not None or page_size is not None:
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        response = client.get("/api/v1/synthetics/tests", params=params)
        if isinstance(response, dict):
            return response.get("results", response.get("data", response.get("items", [])))
        return response if isinstance(response, list) else []
    else:
        return client.get_paginated("/api/v1/synthetics/tests", params=params)


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            monitor_id=dict(type="str", required=False),

            name=dict(type="str", required=False),

            page=dict(type="int", required=False),
            page_size=dict(type="int", required=False),
        )
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
        mutually_exclusive=[
            ("monitor_id", "page"),
            ("monitor_id", "page_size"),
        ],
    )

    result = dict(
        changed=False,
        synthetic_tests=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("monitor_id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["synthetic_tests"] = [item] if item else []
        else:
            result["synthetic_tests"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
