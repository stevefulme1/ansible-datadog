#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Auto-generated from Datadog API spec
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: metric_info
short_description: Retrieve information about metric resources
version_added: "1.0.0"
description:
  - Retrieve a single metric by its identifier, or list all metric resources.
  - This module always reports C(changed=False).
author:
  - "Auto-generated from Datadog API spec"
options:
  id:
    description:
      - The unique identifier of the metric to retrieve.
      - When omitted, all metric resources are listed.
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
- name: Get a specific metric
  stevefulme1.datadog.metric_info:
    id: "example_id"
  register: result

- name: List all metric resources
  stevefulme1.datadog.metric_info:
  register: result



- name: List metric resources with pagination
  stevefulme1.datadog.metric_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
metrics:
  description: List of metric resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:

    description:
      description: >-
        Metric description.
      type: str


    integration:
      description: >-
        Name of the integration that sent the metric if applicable.
      type: str


    per_unit:
      description: >-
        Per unit of the metric such as second in bytes per second.
      type: str


    short_name:
      description: >-
        A more human-readable and abbreviated version of the metric name.
      type: str


    statsd_interval:
      description: >-
        StatsD flush interval of the metric in seconds if applicable.
      type: int


    type:
      description: >-
        Metric type such as gauge or rate.
      type: str


    unit:
      description: >-
        Primary unit of the metric such as byte or operation.
      type: str


"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.datadog.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)


def fetch_single(client, identifier):
    """Retrieve a single metric by identifier."""

    # No single-resource GET endpoint; filter from list
    items = client.get("/api/v1/metrics")
    if isinstance(items, dict):
        items = items.get("results", items.get("data", items.get("items", [])))
    for item in items:
        if str(item.get("id")) == str(identifier):
            return item
    return None



def fetch_list(client, module):
    """List metric resources with optional filtering and pagination."""

    params = {}



















    page = module.params.get("page")
    page_size = module.params.get("page_size")

    if page is not None or page_size is not None:
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        response = client.get("/api/v1/metrics", params=params)
        if isinstance(response, dict):
            return response.get("results", response.get("data", response.get("items", [])))
        return response if isinstance(response, list) else []
    else:
        return client.get_paginated("/api/v1/metrics", params=params)



def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            id=dict(type="str", required=False),
















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
        metrics=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["metrics"] = [item] if item else []
        else:
            result["metrics"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
