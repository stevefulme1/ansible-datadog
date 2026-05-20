#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Auto-generated from Datadog API spec
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: monitor_info
short_description: Retrieve information about monitor resources
version_added: "1.0.0"
description:
  - Retrieve a single monitor by its identifier, or list all monitor resources.
  - This module always reports C(changed=False).
author:
  - "Auto-generated from Datadog API spec"
options:
  id:
    description:
      - The unique identifier of the monitor to retrieve.
      - When omitted, all monitor resources are listed.
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
- name: Get a specific monitor
  stevefulme1.datadog.monitor_info:
    id: "example_id"
  register: result

- name: List all monitor resources
  stevefulme1.datadog.monitor_info:
  register: result


- name: List monitor resources filtered by name
  stevefulme1.datadog.monitor_info:
    name: "my_monitor"
  register: result


- name: List monitor resources with pagination
  stevefulme1.datadog.monitor_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
monitors:
  description: List of monitor resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:

    assets:
      description: >-
        The list of monitor assets tied to a monitor, which represents key links for users to take...
      type: list


    created:
      description: >-
        Timestamp of the monitor creation.
      type: str


    creator:
      description: >-
        Object describing the creator of the shared element.
      type: dict


    deleted:
      description: >-
        Whether or not the monitor is deleted. (Always null)
      type: str


    draft_status:
      description: >-
        Indicates whether the monitor is in a draft or published state. draft: The monitor appears as...
      type: str


    id:
      description: >-
        ID of this monitor.
      type: int


    matching_downtimes:
      description: >-
        A list of active v1 downtimes that match this monitor.
      type: list


    message:
      description: >-
        A message to include with notifications for this monitor.
      type: str


    modified:
      description: >-
        Last timestamp when the monitor was edited.
      type: str


    multi:
      description: >-
        Whether or not the monitor is broken down on different groups.
      type: bool


    name:
      description: >-
        The monitor name.
      type: str


    options:
      description: >-
        List of options associated with your monitor.
      type: dict


    overall_state:
      description: >-
        The different states your monitor can be in.
      type: str


    priority:
      description: >-
        Integer from 1 (high) to 5 (low) indicating alert severity.
      type: int


    query:
      description: >-
        The monitor query.
      type: str


    restricted_roles:
      description: >-
        A list of unique role identifiers to define which roles are allowed to edit the monitor. The...
      type: list


    state:
      description: >-
        Wrapper object with the different monitor states.
      type: dict


    tags:
      description: >-
        Tags associated to your monitor.
      type: list


    type:
      description: >-
        The type of the monitor. For more information about type, see the monitor options docs.
      type: str


"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.datadog.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)


def fetch_single(client, identifier):
    """Retrieve a single monitor by identifier."""

    # No single-resource GET endpoint; filter from list
    items = client.get("/api/v1/monitor")
    if isinstance(items, dict):
        items = items.get("results", items.get("data", items.get("items", [])))
    for item in items:
        if str(item.get("id")) == str(identifier):
            return item
    return None



def fetch_list(client, module):
    """List monitor resources with optional filtering and pagination."""

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
        response = client.get("/api/v1/monitor", params=params)
        if isinstance(response, dict):
            return response.get("results", response.get("data", response.get("items", [])))
        return response if isinstance(response, list) else []
    else:
        return client.get_paginated("/api/v1/monitor", params=params)



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
        monitors=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["monitors"] = [item] if item else []
        else:
            result["monitors"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
