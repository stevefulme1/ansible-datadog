#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Auto-generated from Datadog API spec
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: monitor
short_description: Manage monitors
version_added: "1.0.0"
description:
  - Create, update, and delete monitor resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  state:
    description:
      - Desired state of the monitor resource.
    type: str
    choices: ['present', 'absent']
    default: present

  assets:
    description:
      - >-
        The list of monitor assets tied to a monitor, which represents key links for users to take...
    type: list
    elements: str

  created:
    description:
      - >-
        Timestamp of the monitor creation.
    type: str

  creator:
    description:
      - >-
        Object describing the creator of the shared element.
    type: dict

  deleted:
    description:
      - >-
        Whether or not the monitor is deleted. (Always null)
    type: str

  draft_status:
    description:
      - >-
        Indicates whether the monitor is in a draft or published state. draft: The monitor appears as...
    type: str

    choices: ["draft", "published"]

    default: "published"

  id:
    description:
      - >-
        ID of this monitor.
    type: int

  matching_downtimes:
    description:
      - >-
        A list of active v1 downtimes that match this monitor.
    type: list
    elements: str

  notification_message:
    description:
      - >-
        A message to include with notifications for this monitor.
    type: str

  modified:
    description:
      - >-
        Last timestamp when the monitor was edited.
    type: str

  multi:
    description:
      - >-
        Whether or not the monitor is broken down on different groups.
    type: bool

  name:
    description:
      - >-
        The monitor name.
    type: str

  options:
    description:
      - >-
        List of options associated with your monitor.
    type: dict

  overall_state:
    description:
      - >-
        The different states your monitor can be in.
    type: str

    choices: ["Alert", "Ignored", "No Data", "OK", "Skipped", "Unknown", "Warn"]

  priority:
    description:
      - >-
        Integer from 1 (high) to 5 (low) indicating alert severity.
    type: int

  query:
    description:
      - >-
        The monitor query.
    type: str

  restricted_roles:
    description:
      - >-
        A list of unique role identifiers to define which roles are allowed to edit the monitor. The...
    type: list
    elements: str

  tags:
    description:
      - >-
        Tags associated to your monitor.
    type: list
    elements: str

  type:
    description:
      - >-
        The type of the monitor. For more information about type, see the monitor options docs.
    type: str

    choices: [
        "composite", "event alert", "log alert", "metric alert", "process alert", "query alert",
        "rum alert", "service check", "synthetics alert", "trace-analytics alert", "slo alert",
        "event-v2 alert", "audit alert", "ci-pipelines alert", "ci-tests alert", "error-tracking alert",
        "database-monitoring alert", "network-performance alert", "cost alert", "data-quality alert",
        "network-path alert", "data-jobs alert"
    ]

extends_documentation_fragment:
  - stevefulme1.datadog.auth
"""

EXAMPLES = r"""

- name: Create a monitor
  stevefulme1.datadog.monitor:

    state: present
  # API: POST /api/v1/monitor

- name: Update a monitor
  stevefulme1.datadog.monitor:
    id: "existing_id"

    assets: "updated_assets"

    created: "updated_created"

    creator: "updated_creator"

    deleted: "updated_deleted"

    draft_status: "updated_draft_status"

    matching_downtimes: "updated_matching_downtimes"

    message: "updated_message"

    modified: "updated_modified"

    multi: "updated_multi"

    name: "updated_name"

    options: "updated_options"

    overall_state: "updated_overall_state"

    priority: "updated_priority"

    query: "updated_query"

    restricted_roles: "updated_restricted_roles"

    tags: "updated_tags"

    type: "updated_type"

    state: present
  # API:

- name: Delete a monitor
  stevefulme1.datadog.monitor:
    id: "existing_id"
    state: absent
  # API: DELETE /api/v1/monitor/{monitor_id}

"""

RETURN = r"""

assets:
  description: >-
    The list of monitor assets tied to a monitor, which represents key links for users to take...
  returned: success
  type: list

created:
  description: >-
    Timestamp of the monitor creation.
  returned: success
  type: str

creator:
  description: >-
    Object describing the creator of the shared element.
  returned: success
  type: dict

deleted:
  description: >-
    Whether or not the monitor is deleted. (Always null)
  returned: success
  type: str

draft_status:
  description: >-
    Indicates whether the monitor is in a draft or published state. draft: The monitor appears as...
  returned: success
  type: str

id:
  description: >-
    ID of this monitor.
  returned: success
  type: int

matching_downtimes:
  description: >-
    A list of active v1 downtimes that match this monitor.
  returned: success
  type: list

notification_message:
  description: >-
    A message to include with notifications for this monitor.
  returned: success
  type: str

modified:
  description: >-
    Last timestamp when the monitor was edited.
  returned: success
  type: str

multi:
  description: >-
    Whether or not the monitor is broken down on different groups.
  returned: success
  type: bool

name:
  description: >-
    The monitor name.
  returned: success
  type: str

options:
  description: >-
    List of options associated with your monitor.
  returned: success
  type: dict

overall_state:
  description: >-
    The different states your monitor can be in.
  returned: success
  type: str

priority:
  description: >-
    Integer from 1 (high) to 5 (low) indicating alert severity.
  returned: success
  type: int

query:
  description: >-
    The monitor query.
  returned: success
  type: str

restricted_roles:
  description: >-
    A list of unique role identifiers to define which roles are allowed to edit the monitor. The...
  returned: success
  type: list

state:
  description: >-
    Wrapper object with the different monitor states.
  returned: success
  type: dict

tags:
  description: >-
    Tags associated to your monitor.
  returned: success
  type: list

type:
  description: >-
    The type of the monitor. For more information about type, see the monitor options docs.
  returned: success
  type: str

"""

from ansible_collections.stevefulme1.datadog.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)
from ansible.module_utils.basic import AnsibleModule


def get_current_state(client, module):
    """Retrieve the current state of the monitor via GET."""

    # No single-resource GET endpoint; fall back to list + filter
    identifier = module.params.get("id")

    name = module.params.get("name")
    search_key = "name"
    search_value = name if identifier is None else identifier

    if search_value is None:
        return None
    try:
        items = client.get("/api/v1/monitor")
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

    if module.params.get("assets") is not None:
        payload["assets"] = module.params["assets"]

    if module.params.get("created") is not None:
        payload["created"] = module.params["created"]

    if module.params.get("creator") is not None:
        payload["creator"] = module.params["creator"]

    if module.params.get("deleted") is not None:
        payload["deleted"] = module.params["deleted"]

    if module.params.get("draft_status") is not None:
        payload["draft_status"] = module.params["draft_status"]

    if module.params.get("id") is not None:
        payload["id"] = module.params["id"]

    if module.params.get("matching_downtimes") is not None:
        payload["matching_downtimes"] = module.params["matching_downtimes"]

    if module.params.get("notification_message") is not None:
        payload["message"] = module.params["notification_message"]

    if module.params.get("modified") is not None:
        payload["modified"] = module.params["modified"]

    if module.params.get("multi") is not None:
        payload["multi"] = module.params["multi"]

    if module.params.get("name") is not None:
        payload["name"] = module.params["name"]

    if module.params.get("options") is not None:
        payload["options"] = module.params["options"]

    if module.params.get("overall_state") is not None:
        payload["overall_state"] = module.params["overall_state"]

    if module.params.get("priority") is not None:
        payload["priority"] = module.params["priority"]

    if module.params.get("query") is not None:
        payload["query"] = module.params["query"]

    if module.params.get("restricted_roles") is not None:
        payload["restricted_roles"] = module.params["restricted_roles"]

    if module.params.get("state") is not None:
        payload["state"] = module.params["state"]

    if module.params.get("tags") is not None:
        payload["tags"] = module.params["tags"]

    if module.params.get("type") is not None:
        payload["type"] = module.params["type"]

    return payload


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            assets=dict(
                type="list", elements="str",

            ),

            created=dict(
                type="str",

            ),

            creator=dict(
                type="dict",

            ),

            deleted=dict(
                type="str",

            ),

            draft_status=dict(
                type="str",

                choices=['draft', 'published'],

                default="published",

            ),

            id=dict(
                type="int",

            ),

            matching_downtimes=dict(
                type="list", elements="str",

            ),

            notification_message=dict(
                type="str",

            ),

            modified=dict(
                type="str",

            ),

            multi=dict(
                type="bool",

            ),

            name=dict(
                type="str",

            ),

            options=dict(
                type="dict",

            ),

            overall_state=dict(
                type="str",

                choices=['Alert', 'Ignored', 'No Data', 'OK', 'Skipped', 'Unknown', 'Warn'],

            ),

            priority=dict(
                type="int",

            ),

            query=dict(
                type="str",

            ),

            restricted_roles=dict(
                type="list", elements="str",

            ),

            tags=dict(
                type="list", elements="str",

            ),

            type=dict(
                type="str",

                choices=[
                    'composite', 'event alert', 'log alert', 'metric alert', 'process alert',
                    'query alert', 'rum alert', 'service check', 'synthetics alert',
                    'trace-analytics alert', 'slo alert', 'event-v2 alert', 'audit alert',
                    'ci-pipelines alert', 'ci-tests alert', 'error-tracking alert',
                    'database-monitoring alert', 'network-performance alert', 'cost alert',
                    'data-quality alert', 'network-path alert', 'data-jobs alert'
                ],

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
                        "/api/v1/monitor",
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
                    path = "/api/v1/monitor/{id}".replace(
                        "{id}", str(identifier)
                    )
                    response = client.put(
                        path,
                        data=desired,
                    )
                    result.update(response if isinstance(response, dict) else {})

            else:
                # Resource exists and is up-to-date

                result["assets"] = current.get("assets")

                result["created"] = current.get("created")

                result["creator"] = current.get("creator")

                result["deleted"] = current.get("deleted")

                result["draft_status"] = current.get("draft_status")

                result["id"] = current.get("id")

                result["matching_downtimes"] = current.get("matching_downtimes")

                result["notification_message"] = current.get("message")

                result["modified"] = current.get("modified")

                result["multi"] = current.get("multi")

                result["name"] = current.get("name")

                result["options"] = current.get("options")

                result["overall_state"] = current.get("overall_state")

                result["priority"] = current.get("priority")

                result["query"] = current.get("query")

                result["restricted_roles"] = current.get("restricted_roles")

                result["state"] = current.get("state")

                result["tags"] = current.get("tags")

                result["type"] = current.get("type")

        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "/api/v1/monitor/{monitor_id}".replace(
                        "{id}", str(identifier)
                    )
                    client.delete(path)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
