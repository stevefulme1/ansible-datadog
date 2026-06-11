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
module: downtime
short_description: Manage downtimes
version_added: "1.0.0"
description:
  - Create, update, and delete downtime resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  state:
    description:
      - Desired state of the downtime resource.
    type: str
    choices: ['present', 'absent']
    default: present

  active:
    description:
      - >-
        If a scheduled downtime currently exists.
    type: bool

  active_child:
    description:
      - >-
        The downtime object definition of the active child for the original parent recurring downtime....
    type: dict

  canceled:
    description:
      - >-
        If a scheduled downtime is canceled.
    type: int

  creator_id:
    description:
      - >-
        User ID of the downtime creator.
    type: int

  disabled:
    description:
      - >-
        If a downtime has been disabled.
    type: bool

  downtime_type:
    description:
      - >-
        0 for a downtime applied on or all, 1 when the downtime is only scoped to hosts, or 2 when the...
    type: int

  end:
    description:
      - >-
        POSIX timestamp to end the downtime. If not provided, the downtime is in effect indefinitely...
    type: int

  id:
    description:
      - >-
        The downtime ID.
    type: int

  notification_message:
    description:
      - >-
        A message to include with notifications for this downtime. Email notifications can be sent to...
    type: str

  monitor_id:
    description:
      - >-
        A single monitor to which the downtime applies. If not provided, the downtime applies to all monitors.
    type: int

  monitor_tags:
    description:
      - >-
        A comma-separated list of monitor tags. For example, tags that are applied directly to monitors,...
    type: list
    elements: str

  mute_first_recovery_notification:
    description:
      - >-
        If the first recovery notification during a downtime should be muted.
    type: bool

  notify_end_states:
    description:
      - >-
        States for which notify_end_types sends out notifications for.
    type: list
    elements: str

    default: ["alert", "no data", "warn"]

  notify_end_types:
    description:
      - >-
        If set, notifies if a monitor is in an alert-worthy state (ALERT, WARNING, or NO DATA) when this...
    type: list
    elements: str

    default: ["expired"]

  parent_id:
    description:
      - >-
        ID of the parent Downtime.
    type: int

  recurrence:
    description:
      - >-
        An object defining the recurrence of the downtime.
    type: dict

  scope:
    description:
      - >-
        The scope(s) to which the downtime applies and must be in key:value format. For example,...
    type: list
    elements: str

  start:
    description:
      - >-
        POSIX timestamp to start the downtime. If not provided, the downtime starts the moment it is created.
    type: int

  timezone:
    description:
      - >-
        The timezone in which to display the downtime's start and end times in Datadog applications.
    type: str

  updater_id:
    description:
      - >-
        ID of the last user that updated the downtime.
    type: int

extends_documentation_fragment:
  - stevefulme1.datadog.auth
"""

EXAMPLES = r"""

- name: Create a downtime
  stevefulme1.datadog.downtime:

    state: present
  # API: POST /api/v1/downtime

- name: Update a downtime
  stevefulme1.datadog.downtime:
    id: "existing_id"

    active: "updated_active"

    active_child: "updated_active_child"

    canceled: "updated_canceled"

    creator_id: "updated_creator_id"

    disabled: "updated_disabled"

    downtime_type: "updated_downtime_type"

    end: "updated_end"

    message: "updated_message"

    monitor_id: "updated_monitor_id"

    monitor_tags: "updated_monitor_tags"

    mute_first_recovery_notification: "updated_mute_first_recovery_notification"

    notify_end_states: "updated_notify_end_states"

    notify_end_types: "updated_notify_end_types"

    parent_id: "updated_parent_id"

    recurrence: "updated_recurrence"

    scope: "updated_scope"

    start: "updated_start"

    timezone: "updated_timezone"

    updater_id: "updated_updater_id"

    state: present
  # API:

- name: Delete a downtime
  stevefulme1.datadog.downtime:
    id: "existing_id"
    state: absent
  # API: DELETE /api/v1/downtime/{downtime_id}

"""

RETURN = r"""

active:
  description: >-
    If a scheduled downtime currently exists.
  returned: success
  type: bool

active_child:
  description: >-
    The downtime object definition of the active child for the original parent recurring downtime....
  returned: success
  type: dict

canceled:
  description: >-
    If a scheduled downtime is canceled.
  returned: success
  type: int

creator_id:
  description: >-
    User ID of the downtime creator.
  returned: success
  type: int

disabled:
  description: >-
    If a downtime has been disabled.
  returned: success
  type: bool

downtime_type:
  description: >-
    0 for a downtime applied on or all, 1 when the downtime is only scoped to hosts, or 2 when the...
  returned: success
  type: int

end:
  description: >-
    POSIX timestamp to end the downtime. If not provided, the downtime is in effect indefinitely...
  returned: success
  type: int

id:
  description: >-
    The downtime ID.
  returned: success
  type: int

notification_message:
  description: >-
    A message to include with notifications for this downtime. Email notifications can be sent to...
  returned: success
  type: str

monitor_id:
  description: >-
    A single monitor to which the downtime applies. If not provided, the downtime applies to all monitors.
  returned: success
  type: int

monitor_tags:
  description: >-
    A comma-separated list of monitor tags. For example, tags that are applied directly to monitors,...
  returned: success
  type: list

mute_first_recovery_notification:
  description: >-
    If the first recovery notification during a downtime should be muted.
  returned: success
  type: bool

notify_end_states:
  description: >-
    States for which notify_end_types sends out notifications for.
  returned: success
  type: list

notify_end_types:
  description: >-
    If set, notifies if a monitor is in an alert-worthy state (ALERT, WARNING, or NO DATA) when this...
  returned: success
  type: list

parent_id:
  description: >-
    ID of the parent Downtime.
  returned: success
  type: int

recurrence:
  description: >-
    An object defining the recurrence of the downtime.
  returned: success
  type: dict

scope:
  description: >-
    The scope(s) to which the downtime applies and must be in key:value format. For example,...
  returned: success
  type: list

start:
  description: >-
    POSIX timestamp to start the downtime. If not provided, the downtime starts the moment it is created.
  returned: success
  type: int

timezone:
  description: >-
    The timezone in which to display the downtime's start and end times in Datadog applications.
  returned: success
  type: str

updater_id:
  description: >-
    ID of the last user that updated the downtime.
  returned: success
  type: int

"""


def get_current_state(client, module):
    """Retrieve the current state of the downtime via GET."""

    # No single-resource GET endpoint; fall back to list + filter
    identifier = module.params.get("id")

    search_key = "id"
    search_value = identifier

    if search_value is None:
        return None
    try:
        items = client.get("/api/v1/downtime")
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

    if module.params.get("active") is not None:
        payload["active"] = module.params["active"]

    if module.params.get("active_child") is not None:
        payload["active_child"] = module.params["active_child"]

    if module.params.get("canceled") is not None:
        payload["canceled"] = module.params["canceled"]

    if module.params.get("creator_id") is not None:
        payload["creator_id"] = module.params["creator_id"]

    if module.params.get("disabled") is not None:
        payload["disabled"] = module.params["disabled"]

    if module.params.get("downtime_type") is not None:
        payload["downtime_type"] = module.params["downtime_type"]

    if module.params.get("end") is not None:
        payload["end"] = module.params["end"]

    if module.params.get("id") is not None:
        payload["id"] = module.params["id"]

    if module.params.get("notification_message") is not None:
        payload["message"] = module.params["notification_message"]

    if module.params.get("monitor_id") is not None:
        payload["monitor_id"] = module.params["monitor_id"]

    if module.params.get("monitor_tags") is not None:
        payload["monitor_tags"] = module.params["monitor_tags"]

    if module.params.get("mute_first_recovery_notification") is not None:
        payload["mute_first_recovery_notification"] = module.params["mute_first_recovery_notification"]

    if module.params.get("notify_end_states") is not None:
        payload["notify_end_states"] = module.params["notify_end_states"]

    if module.params.get("notify_end_types") is not None:
        payload["notify_end_types"] = module.params["notify_end_types"]

    if module.params.get("parent_id") is not None:
        payload["parent_id"] = module.params["parent_id"]

    if module.params.get("recurrence") is not None:
        payload["recurrence"] = module.params["recurrence"]

    if module.params.get("scope") is not None:
        payload["scope"] = module.params["scope"]

    if module.params.get("start") is not None:
        payload["start"] = module.params["start"]

    if module.params.get("timezone") is not None:
        payload["timezone"] = module.params["timezone"]

    if module.params.get("updater_id") is not None:
        payload["updater_id"] = module.params["updater_id"]

    return payload


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            active=dict(
                type="bool",

            ),

            active_child=dict(
                type="dict",

            ),

            canceled=dict(
                type="int",

            ),

            creator_id=dict(
                type="int",

            ),

            disabled=dict(
                type="bool",

            ),

            downtime_type=dict(
                type="int",

            ),

            end=dict(
                type="int",

            ),

            id=dict(
                type="int",

            ),

            notification_message=dict(
                type="str",

            ),

            monitor_id=dict(
                type="int",

            ),

            monitor_tags=dict(
                type="list", elements="str",

            ),

            mute_first_recovery_notification=dict(
                type="bool",

            ),

            notify_end_states=dict(
                type="list", elements="str",

                default=["alert", "no data", "warn"],

            ),

            notify_end_types=dict(
                type="list", elements="str",

                default=["expired"],

            ),

            parent_id=dict(
                type="int",

            ),

            recurrence=dict(
                type="dict",

            ),

            scope=dict(
                type="list", elements="str",

            ),

            start=dict(
                type="int",

            ),

            timezone=dict(
                type="str",

            ),

            updater_id=dict(
                type="int",

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
                        "/api/v1/downtime",
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
                    path = "/api/v1/downtime/{id}".replace(
                        "{id}", str(identifier)
                    )
                    response = client.put(
                        path,
                        data=desired,
                    )
                    result.update(response if isinstance(response, dict) else {})

            else:
                # Resource exists and is up-to-date

                result["active"] = current.get("active")

                result["active_child"] = current.get("active_child")

                result["canceled"] = current.get("canceled")

                result["creator_id"] = current.get("creator_id")

                result["disabled"] = current.get("disabled")

                result["downtime_type"] = current.get("downtime_type")

                result["end"] = current.get("end")

                result["id"] = current.get("id")

                result["notification_message"] = current.get("message")

                result["monitor_id"] = current.get("monitor_id")

                result["monitor_tags"] = current.get("monitor_tags")

                result["mute_first_recovery_notification"] = current.get("mute_first_recovery_notification")

                result["notify_end_states"] = current.get("notify_end_states")

                result["notify_end_types"] = current.get("notify_end_types")

                result["parent_id"] = current.get("parent_id")

                result["recurrence"] = current.get("recurrence")

                result["scope"] = current.get("scope")

                result["start"] = current.get("start")

                result["timezone"] = current.get("timezone")

                result["updater_id"] = current.get("updater_id")

        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "/api/v1/downtime/{downtime_id}".replace(
                        "{id}", str(identifier)
                    )
                    client.delete(path)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
