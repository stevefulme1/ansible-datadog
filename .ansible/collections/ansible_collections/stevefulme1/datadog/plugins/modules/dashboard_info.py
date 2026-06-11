#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Auto-generated from Datadog API spec
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dashboard_info
short_description: Retrieve information about dashboard resources
version_added: "1.0.0"
description:
  - Retrieve a single dashboard by its identifier, or list all dashboard resources.
  - This module always reports C(changed=False).
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  id:
    description:
      - The unique identifier of the dashboard to retrieve.
      - When omitted, all dashboard resources are listed.
    type: str
    required: false

  title:
    description:
      - Filter results by title.
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
- name: Get a specific dashboard
  stevefulme1.datadog.dashboard_info:
    id: "example_id"
  register: result

- name: List all dashboard resources
  stevefulme1.datadog.dashboard_info:
  register: result

- name: List dashboard resources filtered by title
  stevefulme1.datadog.dashboard_info:
    title: "my_dashboard"
  register: result

- name: List dashboard resources with pagination
  stevefulme1.datadog.dashboard_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
dashboards:
  description: List of dashboard resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:

    author_handle:
      description: >-
        Identifier of the dashboard author.
      type: str

    author_name:
      description: >-
        Name of the dashboard author.
      type: str

    created_at:
      description: >-
        Creation date of the dashboard.
      type: str

    description:
      description: >-
        Description of the dashboard.
      type: str

    id:
      description: >-
        ID of the dashboard.
      type: str

    is_read_only:
      description: >-
        Whether this dashboard is read-only. If True, only the author and admins can make changes to it....
      type: bool

    layout_type:
      description: >-
        Layout type of the dashboard.
      type: str

    modified_at:
      description: >-
        Modification date of the dashboard.
      type: str

    notify_list:
      description: >-
        List of handles of users to notify when changes are made to this dashboard.
      type: list

    reflow_type:
      description: >-
        Reflow type for a new dashboard layout dashboard. Set this only when layout type is 'ordered'....
      type: str

    restricted_roles:
      description: >-
        A list of role identifiers. Only the author and users associated with at least one of these...
      type: list

    tabs:
      description: >-
        List of tabs for organizing dashboard widgets into groups.
      type: list

    tags:
      description: >-
        List of team names representing ownership of a dashboard.
      type: list

    template_variable_presets:
      description: >-
        Array of template variables saved views.
      type: list

    template_variables:
      description: >-
        List of template variables for this dashboard.
      type: list

    title:
      description: >-
        Title of the dashboard.
      type: str

    url:
      description: >-
        The URL of the dashboard.
      type: str

    widgets:
      description: >-
        List of widgets to display on the dashboard.
      type: list

"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.datadog.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)

def fetch_single(client, identifier):
    """Retrieve a single dashboard by identifier."""

    # No single-resource GET endpoint; filter from list
    items = client.get("/api/v1/dashboard")
    if isinstance(items, dict):
        items = items.get("results", items.get("data", items.get("items", [])))
    for item in items:
        if str(item.get("id")) == str(identifier):
            return item
    return None

def fetch_list(client, module):
    """List dashboard resources with optional filtering and pagination."""

    params = {}

    name_filter = module.params.get("title")
    if name_filter is not None:
        params["title"] = name_filter

    page = module.params.get("page")
    page_size = module.params.get("page_size")

    if page is not None or page_size is not None:
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        response = client.get("/api/v1/dashboard", params=params)
        if isinstance(response, dict):
            return response.get("results", response.get("data", response.get("items", [])))
        return response if isinstance(response, list) else []
    else:
        return client.get_paginated("/api/v1/dashboard", params=params)

def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            id=dict(type="str", required=False),

            title=dict(type="str", required=False),

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
        dashboards=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["dashboards"] = [item] if item else []
        else:
            result["dashboards"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)

if __name__ == "__main__":
    main()
