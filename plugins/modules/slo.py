#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Auto-generated from Datadog API spec
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: slo
short_description: Manage service level objectives
version_added: "1.0.0"
description:
  - Create, update, and delete slo resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Auto-generated from Datadog API spec"
options:
  state:
    description:
      - Desired state of the slo resource.
    type: str
    choices: ['present', 'absent']
    default: present

  name:
    description:
      - >-
        The name of the service level objective object.
    type: str

    required: true





  thresholds:
    description:
      - >-
        The thresholds (timeframes and associated targets) for this service level objective object.
    type: list

    required: true





  type:
    description:
      - >-
        The type of the service level objective.
    type: str

    required: true


    choices: ["metric", "monitor", "time_slice"]




  created_at:
    description:
      - >-
        Creation timestamp (UNIX time in seconds) Always included in service level objective responses.
    type: int





  creator:
    description:
      - >-
        Object describing the creator of the shared element.
    type: dict





  description:
    description:
      - >-
        A user-defined description of the service level objective. Always included in service level...
    type: str





  groups:
    description:
      - >-
        A list of (up to 100) monitor groups that narrow the scope of a monitor service level objective....
    type: list





  id:
    description:
      - >-
        A unique identifier for the service level objective object. Always included in service level...
    type: str





  modified_at:
    description:
      - >-
        Modification timestamp (UNIX time in seconds) Always included in service level objective responses.
    type: int





  monitor_ids:
    description:
      - >-
        A list of monitor ids that defines the scope of a monitor service level objective. Required if...
    type: list





  monitor_tags:
    description:
      - >-
        The union of monitor tags for all monitors referenced by the monitor_ids field. Always included...
    type: list





  query:
    description:
      - >-
        A count-based (metric) SLO query. This field is superseded by sli_specification but is retained...
    type: dict





  sli_specification:
    description:
      - >-
        A time-slice SLI specification.
    type: dict





  tags:
    description:
      - >-
        A list of tags associated with this service level objective. Always included in service level...
    type: list





  target_threshold:
    description:
      - >-
        The target threshold such that when the service level indicator is above this threshold over the...
    type: float





  timeframe:
    description:
      - >-
        The SLO time window options. Note that "custom" is not a valid option for creating or updating...
    type: str


    choices: ["7d", "30d", "90d", "custom"]




  warning_threshold:
    description:
      - >-
        The optional warning threshold such that when the service level indicator is below this value...
    type: float





extends_documentation_fragment:
  - stevefulme1.datadog.auth
"""

EXAMPLES = r"""

- name: Create a slo
  stevefulme1.datadog.slo:


    name: "example_name"



    thresholds: "example_thresholds"



    type: "example_type"






























    state: present
  # API: POST /api/v1/slo



- name: Update a slo
  stevefulme1.datadog.slo:
    id: "existing_id"








    created_at: "updated_created_at"



    creator: "updated_creator"



    description: "updated_description"



    groups: "updated_groups"





    modified_at: "updated_modified_at"



    monitor_ids: "updated_monitor_ids"



    monitor_tags: "updated_monitor_tags"



    query: "updated_query"



    sli_specification: "updated_sli_specification"



    tags: "updated_tags"



    target_threshold: "updated_target_threshold"



    timeframe: "updated_timeframe"



    warning_threshold: "updated_warning_threshold"


    state: present
  # API:  



- name: Delete a slo
  stevefulme1.datadog.slo:
    id: "existing_id"
    state: absent
  # API: DELETE /api/v1/slo/{slo_id}

"""

RETURN = r"""

configured_alert_ids:
  description: >-
    A list of SLO monitors IDs that reference this SLO. This field is returned only when...
  returned: success
  type: list


created_at:
  description: >-
    Creation timestamp (UNIX time in seconds) Always included in service level objective responses.
  returned: success
  type: int


creator:
  description: >-
    Object describing the creator of the shared element.
  returned: success
  type: dict


description:
  description: >-
    A user-defined description of the service level objective. Always included in service level...
  returned: success
  type: str


groups:
  description: >-
    A list of (up to 20) monitor groups that narrow the scope of a monitor service level objective....
  returned: success
  type: list


id:
  description: >-
    A unique identifier for the service level objective object. Always included in service level...
  returned: success
  type: str


modified_at:
  description: >-
    Modification timestamp (UNIX time in seconds) Always included in service level objective responses.
  returned: success
  type: int


monitor_ids:
  description: >-
    A list of monitor ids that defines the scope of a monitor service level objective. Required if...
  returned: success
  type: list


monitor_tags:
  description: >-
    The union of monitor tags for all monitors referenced by the monitor_ids field. Always included...
  returned: success
  type: list


name:
  description: >-
    The name of the service level objective object.
  returned: success
  type: str


query:
  description: >-
    A count-based (metric) SLO query. This field is superseded by sli_specification but is retained...
  returned: success
  type: dict


sli_specification:
  description: >-
    A time-slice SLI specification.
  returned: success
  type: dict


tags:
  description: >-
    A list of tags associated with this service level objective. Always included in service level...
  returned: success
  type: list


target_threshold:
  description: >-
    The target threshold such that when the service level indicator is above this threshold over the...
  returned: success
  type: float


thresholds:
  description: >-
    The thresholds (timeframes and associated targets) for this service level objective object.
  returned: success
  type: list


timeframe:
  description: >-
    The SLO time window options. Note that "custom" is not a valid option for creating or updating...
  returned: success
  type: str


type:
  description: >-
    The type of the service level objective.
  returned: success
  type: str


warning_threshold:
  description: >-
    The optional warning threshold such that when the service level indicator is below this value...
  returned: success
  type: float


"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.datadog.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)


def get_current_state(client, module):
    """Retrieve the current state of the slo via GET."""

    # No single-resource GET endpoint; fall back to list + filter
    identifier = module.params.get("id")

    name = module.params.get("name")
    search_key = "name"
    search_value = name if identifier is None else identifier

    if search_value is None:
        return None
    try:
        items = client.get("/api/v1/slo")
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

    if module.params.get("name") is not None:
        payload["name"] = module.params["name"]

    if module.params.get("thresholds") is not None:
        payload["thresholds"] = module.params["thresholds"]

    if module.params.get("type") is not None:
        payload["type"] = module.params["type"]

    if module.params.get("created_at") is not None:
        payload["created_at"] = module.params["created_at"]

    if module.params.get("creator") is not None:
        payload["creator"] = module.params["creator"]

    if module.params.get("description") is not None:
        payload["description"] = module.params["description"]

    if module.params.get("groups") is not None:
        payload["groups"] = module.params["groups"]

    if module.params.get("id") is not None:
        payload["id"] = module.params["id"]

    if module.params.get("modified_at") is not None:
        payload["modified_at"] = module.params["modified_at"]

    if module.params.get("monitor_ids") is not None:
        payload["monitor_ids"] = module.params["monitor_ids"]

    if module.params.get("monitor_tags") is not None:
        payload["monitor_tags"] = module.params["monitor_tags"]

    if module.params.get("query") is not None:
        payload["query"] = module.params["query"]

    if module.params.get("sli_specification") is not None:
        payload["sli_specification"] = module.params["sli_specification"]

    if module.params.get("tags") is not None:
        payload["tags"] = module.params["tags"]

    if module.params.get("target_threshold") is not None:
        payload["target_threshold"] = module.params["target_threshold"]

    if module.params.get("timeframe") is not None:
        payload["timeframe"] = module.params["timeframe"]

    if module.params.get("warning_threshold") is not None:
        payload["warning_threshold"] = module.params["warning_threshold"]

    return payload


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            name=dict(
                type="str",

                required=True,





            ),

            thresholds=dict(
                type="list",

                required=True,





            ),

            type=dict(
                type="str",

                required=True,


                choices=['metric', 'monitor', 'time_slice'],




            ),

            created_at=dict(
                type="int",





            ),

            creator=dict(
                type="dict",





            ),

            description=dict(
                type="str",





            ),

            groups=dict(
                type="list",





            ),

            id=dict(
                type="str",





            ),

            modified_at=dict(
                type="int",





            ),

            monitor_ids=dict(
                type="list",





            ),

            monitor_tags=dict(
                type="list",





            ),

            query=dict(
                type="dict",





            ),

            sli_specification=dict(
                type="dict",





            ),

            tags=dict(
                type="list",





            ),

            target_threshold=dict(
                type="float",





            ),

            timeframe=dict(
                type="str",


                choices=['7d', '30d', '90d', 'custom'],




            ),

            warning_threshold=dict(
                type="float",





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

                    response = client.POST(
                        "/api/v1/slo",
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
                    path = "".replace(
                        "{id}", str(identifier)
                    )
                    response = client.put(
                        path,
                        data=desired,
                    )
                    result.update(response if isinstance(response, dict) else {})


            else:
                # Resource exists and is up-to-date

                result["configured_alert_ids"] = current.get("configured_alert_ids")

                result["created_at"] = current.get("created_at")

                result["creator"] = current.get("creator")

                result["description"] = current.get("description")

                result["groups"] = current.get("groups")

                result["id"] = current.get("id")

                result["modified_at"] = current.get("modified_at")

                result["monitor_ids"] = current.get("monitor_ids")

                result["monitor_tags"] = current.get("monitor_tags")

                result["name"] = current.get("name")

                result["query"] = current.get("query")

                result["sli_specification"] = current.get("sli_specification")

                result["tags"] = current.get("tags")

                result["target_threshold"] = current.get("target_threshold")

                result["thresholds"] = current.get("thresholds")

                result["timeframe"] = current.get("timeframe")

                result["type"] = current.get("type")

                result["warning_threshold"] = current.get("warning_threshold")


        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "/api/v1/slo/{slo_id}".replace(
                        "{id}", str(identifier)
                    )
                    client.delete(path)


    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
