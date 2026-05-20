#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Auto-generated from Datadog API spec
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: slo_info
short_description: Retrieve information about slo resources
version_added: "1.0.0"
description:
  - Retrieve a single slo by its identifier, or list all slo resources.
  - This module always reports C(changed=False).
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  id:
    description:
      - The unique identifier of the slo to retrieve.
      - When omitted, all slo resources are listed.
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
- name: Get a specific slo
  stevefulme1.datadog.slo_info:
    id: "example_id"
  register: result

- name: List all slo resources
  stevefulme1.datadog.slo_info:
  register: result


- name: List slo resources filtered by name
  stevefulme1.datadog.slo_info:
    name: "my_slo"
  register: result


- name: List slo resources with pagination
  stevefulme1.datadog.slo_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
slos:
  description: List of slo resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:

    configured_alert_ids:
      description: >-
        A list of SLO monitors IDs that reference this SLO. This field is returned only when...
      type: list


    created_at:
      description: >-
        Creation timestamp (UNIX time in seconds) Always included in service level objective responses.
      type: int


    creator:
      description: >-
        Object describing the creator of the shared element.
      type: dict


    description:
      description: >-
        A user-defined description of the service level objective. Always included in service level...
      type: str


    groups:
      description: >-
        A list of (up to 20) monitor groups that narrow the scope of a monitor service level objective....
      type: list


    id:
      description: >-
        A unique identifier for the service level objective object. Always included in service level...
      type: str


    modified_at:
      description: >-
        Modification timestamp (UNIX time in seconds) Always included in service level objective responses.
      type: int


    monitor_ids:
      description: >-
        A list of monitor ids that defines the scope of a monitor service level objective. Required if...
      type: list


    monitor_tags:
      description: >-
        The union of monitor tags for all monitors referenced by the monitor_ids field. Always included...
      type: list


    name:
      description: >-
        The name of the service level objective object.
      type: str


    query:
      description: >-
        A count-based (metric) SLO query. This field is superseded by sli_specification but is retained...
      type: dict


    sli_specification:
      description: >-
        A time-slice SLI specification.
      type: dict


    tags:
      description: >-
        A list of tags associated with this service level objective. Always included in service level...
      type: list


    target_threshold:
      description: >-
        The target threshold such that when the service level indicator is above this threshold over the...
      type: float


    thresholds:
      description: >-
        The thresholds (timeframes and associated targets) for this service level objective object.
      type: list


    timeframe:
      description: >-
        The SLO time window options. Note that "custom" is not a valid option for creating or updating...
      type: str


    type:
      description: >-
        The type of the service level objective.
      type: str


    warning_threshold:
      description: >-
        The optional warning threshold such that when the service level indicator is below this value...
      type: float


"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.datadog.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)


def fetch_single(client, identifier):
    """Retrieve a single slo by identifier."""

    # No single-resource GET endpoint; filter from list
    items = client.get("/api/v1/slo")
    if isinstance(items, dict):
        items = items.get("results", items.get("data", items.get("items", [])))
    for item in items:
        if str(item.get("id")) == str(identifier):
            return item
    return None



def fetch_list(client, module):
    """List slo resources with optional filtering and pagination."""

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
        response = client.get("/api/v1/slo", params=params)
        if isinstance(response, dict):
            return response.get("results", response.get("data", response.get("items", [])))
        return response if isinstance(response, list) else []
    else:
        return client.get_paginated("/api/v1/slo", params=params)



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
        slos=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["slos"] = [item] if item else []
        else:
            result["slos"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
