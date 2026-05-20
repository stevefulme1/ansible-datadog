#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Auto-generated from Datadog API spec
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: downtime_info
short_description: Retrieve information about downtime resources
version_added: "1.0.0"
description:
  - Retrieve a single downtime by its identifier, or list all downtime resources.
  - This module always reports C(changed=False).
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  id:
    description:
      - The unique identifier of the downtime to retrieve.
      - When omitted, all downtime resources are listed.
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
- name: Get a specific downtime
  stevefulme1.datadog.downtime_info:
    id: "example_id"
  register: result

- name: List all downtime resources
  stevefulme1.datadog.downtime_info:
  register: result



- name: List downtime resources with pagination
  stevefulme1.datadog.downtime_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
downtimes:
  description: List of downtime resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:

    active:
      description: >-
        If a scheduled downtime currently exists.
      type: bool


    active_child:
      description: >-
        The downtime object definition of the active child for the original parent recurring downtime....
      type: dict


    canceled:
      description: >-
        If a scheduled downtime is canceled.
      type: int


    creator_id:
      description: >-
        User ID of the downtime creator.
      type: int


    disabled:
      description: >-
        If a downtime has been disabled.
      type: bool


    downtime_type:
      description: >-
        0 for a downtime applied on or all, 1 when the downtime is only scoped to hosts, or 2 when the...
      type: int


    end:
      description: >-
        POSIX timestamp to end the downtime. If not provided, the downtime is in effect indefinitely...
      type: int


    id:
      description: >-
        The downtime ID.
      type: int


    message:
      description: >-
        A message to include with notifications for this downtime. Email notifications can be sent to...
      type: str


    monitor_id:
      description: >-
        A single monitor to which the downtime applies. If not provided, the downtime applies to all monitors.
      type: int


    monitor_tags:
      description: >-
        A comma-separated list of monitor tags. For example, tags that are applied directly to monitors,...
      type: list


    mute_first_recovery_notification:
      description: >-
        If the first recovery notification during a downtime should be muted.
      type: bool


    notify_end_states:
      description: >-
        States for which notify_end_types sends out notifications for.
      type: list


    notify_end_types:
      description: >-
        If set, notifies if a monitor is in an alert-worthy state (ALERT, WARNING, or NO DATA) when this...
      type: list


    parent_id:
      description: >-
        ID of the parent Downtime.
      type: int


    recurrence:
      description: >-
        An object defining the recurrence of the downtime.
      type: dict


    scope:
      description: >-
        The scope(s) to which the downtime applies and must be in key:value format. For example,...
      type: list


    start:
      description: >-
        POSIX timestamp to start the downtime. If not provided, the downtime starts the moment it is created.
      type: int


    timezone:
      description: >-
        The timezone in which to display the downtime's start and end times in Datadog applications.
      type: str


    updater_id:
      description: >-
        ID of the last user that updated the downtime.
      type: int


"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.datadog.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)


def fetch_single(client, identifier):
    """Retrieve a single downtime by identifier."""

    # No single-resource GET endpoint; filter from list
    items = client.get("/api/v1/downtime")
    if isinstance(items, dict):
        items = items.get("results", items.get("data", items.get("items", [])))
    for item in items:
        if str(item.get("id")) == str(identifier):
            return item
    return None



def fetch_list(client, module):
    """List downtime resources with optional filtering and pagination."""

    params = {}













































    page = module.params.get("page")
    page_size = module.params.get("page_size")

    if page is not None or page_size is not None:
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        response = client.get("/api/v1/downtime", params=params)
        if isinstance(response, dict):
            return response.get("results", response.get("data", response.get("items", [])))
        return response if isinstance(response, list) else []
    else:
        return client.get_paginated("/api/v1/downtime", params=params)



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
        downtimes=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["downtimes"] = [item] if item else []
        else:
            result["downtimes"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
