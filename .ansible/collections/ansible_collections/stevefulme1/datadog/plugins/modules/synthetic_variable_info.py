#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Auto-generated from Datadog API spec
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: synthetic_variable_info
short_description: Retrieve information about synthetic_variable resources
version_added: "1.0.0"
description:
  - Retrieve a single synthetic_variable by its identifier, or list all synthetic_variable resources.
  - This module always reports C(changed=False).
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  id:
    description:
      - The unique identifier of the synthetic_variable to retrieve.
      - When omitted, all synthetic_variable resources are listed.
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
- name: Get a specific synthetic_variable
  stevefulme1.datadog.synthetic_variable_info:
    id: "example_id"
  register: result

- name: List all synthetic_variable resources
  stevefulme1.datadog.synthetic_variable_info:
  register: result

- name: List synthetic_variable resources filtered by name
  stevefulme1.datadog.synthetic_variable_info:
    name: "my_synthetic_variable"
  register: result

- name: List synthetic_variable resources with pagination
  stevefulme1.datadog.synthetic_variable_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
synthetic_variables:
  description: List of synthetic_variable resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:

    attributes:
      description: >-
        Attributes of the global variable.
      type: dict

    description:
      description: >-
        Description of the global variable.
      type: str

    id:
      description: >-
        Unique identifier of the global variable.
      type: str

    is_fido:
      description: >-
        Determines if the global variable is a FIDO variable.
      type: bool

    is_totp:
      description: >-
        Determines if the global variable is a TOTP/MFA variable.
      type: bool

    name:
      description: >-
        Name of the global variable. Unique across Synthetic global variables.
      type: str

    parse_test_options:
      description: >-
        Parser options to use for retrieving a Synthetic global variable from a Synthetic test. Used in...
      type: dict

    parse_test_public_id:
      description: >-
        A Synthetic test ID to use as a test to generate the variable value.
      type: str

    tags:
      description: >-
        Tags of the global variable.
      type: list

    value:
      description: >-
        Value of the global variable.
      type: dict

"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.datadog.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)

def fetch_single(client, identifier):
    """Retrieve a single synthetic_variable by identifier."""

    # No single-resource GET endpoint; filter from list
    items = client.get("/api/v1/synthetics/variables")
    if isinstance(items, dict):
        items = items.get("results", items.get("data", items.get("items", [])))
    for item in items:
        if str(item.get("id")) == str(identifier):
            return item
    return None

def fetch_list(client, module):
    """List synthetic_variable resources with optional filtering and pagination."""

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
        response = client.get("/api/v1/synthetics/variables", params=params)
        if isinstance(response, dict):
            return response.get("results", response.get("data", response.get("items", [])))
        return response if isinstance(response, list) else []
    else:
        return client.get_paginated("/api/v1/synthetics/variables", params=params)

def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            id=dict(type="str", required=False),

            name=dict(type="str", required=False),

            page=dict(type="int", required=False),
            page_size=dict(type="int", required=False),
        )
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
        mutually_exclusive=[
            ("id", "page"),
            ("id", "page_size"),
        ],
    )

    result = dict(
        changed=False,
        synthetic_variables=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["synthetic_variables"] = [item] if item else []
        else:
            result["synthetic_variables"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)

if __name__ == "__main__":
    main()
