#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Auto-generated from Datadog API spec
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: config_indexe_info
short_description: Retrieve information about config_indexe resources
version_added: "1.0.0"
description:
  - Retrieve a single config_indexe by its identifier, or list all config_indexe resources.
  - This module always reports C(changed=False).
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  id:
    description:
      - The unique identifier of the config_indexe to retrieve.
      - When omitted, all config_indexe resources are listed.
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
- name: Get a specific config_indexe
  stevefulme1.datadog.config_indexe_info:
    id: "example_id"
  register: result

- name: List all config_indexe resources
  stevefulme1.datadog.config_indexe_info:
  register: result

- name: List config_indexe resources filtered by name
  stevefulme1.datadog.config_indexe_info:
    name: "my_config_indexe"
  register: result

- name: List config_indexe resources with pagination
  stevefulme1.datadog.config_indexe_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
config_indexes:
  description: List of config_indexe resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:

    daily_limit:
      description: >-
        The number of log events you can send in this index per day before you are rate-limited.
      type: int

    daily_limit_reset:
      description: >-
        Object containing options to override the default daily limit reset time.
      type: dict

    daily_limit_warning_threshold_percentage:
      description: >-
        A percentage threshold of the daily quota at which a Datadog warning event is generated.
      type: float

    exclusion_filters:
      description: >-
        An array of exclusion objects. The logs are tested against the query of each filter, following...
      type: list

    filter:
      description: >-
        Filter for logs.
      type: dict

    is_rate_limited:
      description: >-
        A boolean stating if the index is rate limited, meaning more logs than the daily limit have been...
      type: bool

    name:
      description: >-
        The name of the index.
      type: str

    num_flex_logs_retention_days:
      description: >-
        The total number of days logs are stored in Standard and Flex Tier before being deleted from the...
      type: int

    num_retention_days:
      description: >-
        The number of days logs are stored in Standard Tier before aging into the Flex Tier or being...
      type: int

    tags:
      description: >-
        A list of tags associated with the index. Tags must be in key:value format.
      type: list

"""

from ansible_collections.stevefulme1.datadog.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)
from ansible.module_utils.basic import AnsibleModule


def fetch_single(client, identifier):
    """Retrieve a single config_indexe by identifier."""

    # No single-resource GET endpoint; filter from list
    items = client.get("/api/v1/logs/config/indexes")
    if isinstance(items, dict):
        items = items.get("results", items.get("data", items.get("items", [])))
    for item in items:
        if str(item.get("id")) == str(identifier):
            return item
    return None


def fetch_list(client, module):
    """List config_indexe resources with optional filtering and pagination."""

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
        response = client.get("/api/v1/logs/config/indexes", params=params)
        if isinstance(response, dict):
            return response.get("results", response.get("data", response.get("items", [])))
        return response if isinstance(response, list) else []
    else:
        return client.get_paginated("/api/v1/logs/config/indexes", params=params)


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
        config_indexes=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["config_indexes"] = [item] if item else []
        else:
            result["config_indexes"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
