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
module: dashboard
short_description: Manage dashboards
version_added: "1.0.0"
description:
  - Create, update, and delete dashboard resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  state:
    description:
      - Desired state of the dashboard resource.
    type: str
    choices: ['present', 'absent']
    default: present

  data:
    description:
      - >-
        List of dashboard bulk action request data objects.
    type: list
    elements: str

    required: true

  layout_type:
    description:
      - >-
        Layout type of the dashboard.
    type: str

    required: true

    choices: ["ordered", "free"]

  title:
    description:
      - >-
        Title of the dashboard.
    type: str

    required: true

  widgets:
    description:
      - >-
        List of widgets to display on the dashboard.
    type: list
    elements: str

    required: true

  author_handle:
    description:
      - >-
        Identifier of the dashboard author.
    type: str

  author_name:
    description:
      - >-
        Name of the dashboard author.
    type: str

  created_at:
    description:
      - >-
        Creation date of the dashboard.
    type: str

  description:
    description:
      - >-
        Description of the dashboard.
    type: str

  id:
    description:
      - >-
        ID of the dashboard.
    type: str

  is_read_only:
    description:
      - >-
        Whether this dashboard is read-only. If True, only the author and admins can make changes to it....
    type: bool

  modified_at:
    description:
      - >-
        Modification date of the dashboard.
    type: str

  notify_list:
    description:
      - >-
        List of handles of users to notify when changes are made to this dashboard.
    type: list
    elements: str

  reflow_type:
    description:
      - >-
        Reflow type for a new dashboard layout dashboard. Set this only when layout type is 'ordered'....
    type: str

    choices: ["auto", "fixed"]

  restricted_roles:
    description:
      - >-
        A list of role identifiers. Only the author and users associated with at least one of these...
    type: list
    elements: str

  tabs:
    description:
      - >-
        List of tabs for organizing dashboard widgets into groups.
    type: list
    elements: str

  tags:
    description:
      - >-
        List of team names representing ownership of a dashboard.
    type: list
    elements: str

  template_variable_presets:
    description:
      - >-
        Array of template variables saved views.
    type: list
    elements: str

  template_variables:
    description:
      - >-
        List of template variables for this dashboard.
    type: list
    elements: str

  url:
    description:
      - >-
        The URL of the dashboard.
    type: str

extends_documentation_fragment:
  - stevefulme1.datadog.auth
"""

EXAMPLES = r"""

- name: Create a dashboard
  stevefulme1.datadog.dashboard:

    data: "example_data"

    layout_type: "example_layout_type"

    title: "example_title"

    widgets: "example_widgets"

    state: present
  # API: POST /api/v1/dashboard

- name: Update a dashboard
  stevefulme1.datadog.dashboard:
    id: "existing_id"

    author_handle: "updated_author_handle"

    author_name: "updated_author_name"

    created_at: "updated_created_at"

    description: "updated_description"

    is_read_only: "updated_is_read_only"

    modified_at: "updated_modified_at"

    notify_list: "updated_notify_list"

    reflow_type: "updated_reflow_type"

    restricted_roles: "updated_restricted_roles"

    tabs: "updated_tabs"

    tags: "updated_tags"

    template_variable_presets: "updated_template_variable_presets"

    template_variables: "updated_template_variables"

    url: "updated_url"

    state: present
  # API:

- name: Delete a dashboard
  stevefulme1.datadog.dashboard:
    id: "existing_id"
    state: absent
  # API: DELETE /api/v1/dashboard/{dashboard_id}

"""

RETURN = r"""

author_handle:
  description: >-
    Identifier of the dashboard author.
  returned: success
  type: str

author_name:
  description: >-
    Name of the dashboard author.
  returned: success
  type: str

created_at:
  description: >-
    Creation date of the dashboard.
  returned: success
  type: str

description:
  description: >-
    Description of the dashboard.
  returned: success
  type: str

id:
  description: >-
    ID of the dashboard.
  returned: success
  type: str

is_read_only:
  description: >-
    Whether this dashboard is read-only. If True, only the author and admins can make changes to it....
  returned: success
  type: bool

layout_type:
  description: >-
    Layout type of the dashboard.
  returned: success
  type: str

modified_at:
  description: >-
    Modification date of the dashboard.
  returned: success
  type: str

notify_list:
  description: >-
    List of handles of users to notify when changes are made to this dashboard.
  returned: success
  type: list

reflow_type:
  description: >-
    Reflow type for a new dashboard layout dashboard. Set this only when layout type is 'ordered'....
  returned: success
  type: str

restricted_roles:
  description: >-
    A list of role identifiers. Only the author and users associated with at least one of these...
  returned: success
  type: list

tabs:
  description: >-
    List of tabs for organizing dashboard widgets into groups.
  returned: success
  type: list

tags:
  description: >-
    List of team names representing ownership of a dashboard.
  returned: success
  type: list

template_variable_presets:
  description: >-
    Array of template variables saved views.
  returned: success
  type: list

template_variables:
  description: >-
    List of template variables for this dashboard.
  returned: success
  type: list

title:
  description: >-
    Title of the dashboard.
  returned: success
  type: str

url:
  description: >-
    The URL of the dashboard.
  returned: success
  type: str

widgets:
  description: >-
    List of widgets to display on the dashboard.
  returned: success
  type: list

"""


def get_current_state(client, module):
    """Retrieve the current state of the dashboard via GET."""

    # No single-resource GET endpoint; fall back to list + filter
    identifier = module.params.get("id")

    name = module.params.get("title")
    search_key = "title"
    search_value = name if identifier is None else identifier

    if search_value is None:
        return None
    try:
        items = client.get("/api/v1/dashboard")
        if isinstance(items, dict):
            items = items.get("results", items.get("data", items.get("items", [])))
        for item in items:
            if str(item.get(search_key)) == str(search_value):
                return item
            if str(item.get("id")) == str(search_value):
                return item
        return None
    except ClientError:
        return None


def needs_update(current, desired):
    """Compare current state against desired params and return True if an update is needed."""
    if current is None:
        return True
    for key, value in desired.items():
        if value is None:
            continue
        current_value = current.get(key)
        if current_value != value:
            return True
    return False


def build_payload(module):
    """Build the API request payload from module params."""
    payload = {}

    if module.params.get("data") is not None:
        payload["data"] = module.params["data"]

    if module.params.get("layout_type") is not None:
        payload["layout_type"] = module.params["layout_type"]

    if module.params.get("title") is not None:
        payload["title"] = module.params["title"]

    if module.params.get("widgets") is not None:
        payload["widgets"] = module.params["widgets"]

    if module.params.get("author_handle") is not None:
        payload["author_handle"] = module.params["author_handle"]

    if module.params.get("author_name") is not None:
        payload["author_name"] = module.params["author_name"]

    if module.params.get("created_at") is not None:
        payload["created_at"] = module.params["created_at"]

    if module.params.get("description") is not None:
        payload["description"] = module.params["description"]

    if module.params.get("id") is not None:
        payload["id"] = module.params["id"]

    if module.params.get("is_read_only") is not None:
        payload["is_read_only"] = module.params["is_read_only"]

    if module.params.get("modified_at") is not None:
        payload["modified_at"] = module.params["modified_at"]

    if module.params.get("notify_list") is not None:
        payload["notify_list"] = module.params["notify_list"]

    if module.params.get("reflow_type") is not None:
        payload["reflow_type"] = module.params["reflow_type"]

    if module.params.get("restricted_roles") is not None:
        payload["restricted_roles"] = module.params["restricted_roles"]

    if module.params.get("tabs") is not None:
        payload["tabs"] = module.params["tabs"]

    if module.params.get("tags") is not None:
        payload["tags"] = module.params["tags"]

    if module.params.get("template_variable_presets") is not None:
        payload["template_variable_presets"] = module.params["template_variable_presets"]

    if module.params.get("template_variables") is not None:
        payload["template_variables"] = module.params["template_variables"]

    if module.params.get("url") is not None:
        payload["url"] = module.params["url"]

    return payload


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            data=dict(
                type="list", elements="str",

                required=True,

            ),

            layout_type=dict(
                type="str",

                required=True,

                choices=['ordered', 'free'],

            ),

            title=dict(
                type="str",

                required=True,

            ),

            widgets=dict(
                type="list", elements="str",

                required=True,

            ),

            author_handle=dict(
                type="str",

            ),

            author_name=dict(
                type="str",

            ),

            created_at=dict(
                type="str",

            ),

            description=dict(
                type="str",

            ),

            id=dict(
                type="str",

            ),

            is_read_only=dict(
                type="bool",

            ),

            modified_at=dict(
                type="str",

            ),

            notify_list=dict(
                type="list", elements="str",

            ),

            reflow_type=dict(
                type="str",

                choices=['auto', 'fixed'],

            ),

            restricted_roles=dict(
                type="list", elements="str",

            ),

            tabs=dict(
                type="list", elements="str",

            ),

            tags=dict(
                type="list", elements="str",

            ),

            template_variable_presets=dict(
                type="list", elements="str",

            ),

            template_variables=dict(
                type="list", elements="str",

            ),

            url=dict(
                type="str",

            ),

        )
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,

    )

    state = module.params["state"]
    result = dict(changed=False, diff=dict(before={}, after={}))

    try:
        client = Client(module)
        current = get_current_state(client, module)

        if state == "present":
            desired = build_payload(module)

            if current is None:
                # Resource does not exist — create it
                result["changed"] = True
                result["diff"]["before"] = {}
                result["diff"]["after"] = desired

                if not module.check_mode:

                    response = client.post(
                        "/api/v1/dashboard",
                        data=desired,
                    )
                    result.update(response if isinstance(response, dict) else {})

            elif needs_update(current, desired):
                # Resource exists but needs updating
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = dict(current, **{k: v for k, v in desired.items() if v is not None})

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "/api/v1/dashboard/{id}".replace(
                        "{id}", str(identifier)
                    )
                    response = client.put(
                        path,
                        data=desired,
                    )
                    result.update(response if isinstance(response, dict) else {})

            else:
                # Resource exists and is up-to-date

                result["author_handle"] = current.get("author_handle")

                result["author_name"] = current.get("author_name")

                result["created_at"] = current.get("created_at")

                result["description"] = current.get("description")

                result["id"] = current.get("id")

                result["is_read_only"] = current.get("is_read_only")

                result["layout_type"] = current.get("layout_type")

                result["modified_at"] = current.get("modified_at")

                result["notify_list"] = current.get("notify_list")

                result["reflow_type"] = current.get("reflow_type")

                result["restricted_roles"] = current.get("restricted_roles")

                result["tabs"] = current.get("tabs")

                result["tags"] = current.get("tags")

                result["template_variable_presets"] = current.get("template_variable_presets")

                result["template_variables"] = current.get("template_variables")

                result["title"] = current.get("title")

                result["url"] = current.get("url")

                result["widgets"] = current.get("widgets")

        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "/api/v1/dashboard/{dashboard_id}".replace(
                        "{id}", str(identifier)
                    )
                    client.delete(path)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
