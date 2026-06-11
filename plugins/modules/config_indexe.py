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
module: config_indexe
short_description: Manage logs indexes
version_added: "1.0.0"
description:
  - Create, update, and delete config_indexe resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  state:
    description:
      - Desired state of the config_indexe resource.
    type: str
    choices: ['present', 'absent']
    default: present

  filter:
    description:
      - >-
        Filter for logs.
    type: dict

    required: true

  name:
    description:
      - >-
        The name of the index.
    type: str

    required: true

  daily_limit:
    description:
      - >-
        The number of log events you can send in this index per day before you are rate-limited.
    type: int

  daily_limit_reset:
    description:
      - >-
        Object containing options to override the default daily limit reset time.
    type: dict

  daily_limit_warning_threshold_percentage:
    description:
      - >-
        A percentage threshold of the daily quota at which a Datadog warning event is generated.
    type: float

  disable_daily_limit:
    description:
      - >-
        If true, sets the daily_limit value to null and the index is not limited on a daily basis (any...
    type: bool

  exclusion_filters:
    description:
      - >-
        An array of exclusion objects. The logs are tested against the query of each filter, following...
    type: list
    elements: str

  is_rate_limited:
    description:
      - >-
        A boolean stating if the index is rate limited, meaning more logs than the daily limit have been...
    type: bool

  num_flex_logs_retention_days:
    description:
      - >-
        The total number of days logs are stored in Standard and Flex Tier before being deleted from the...
    type: int

  num_retention_days:
    description:
      - >-
        The number of days logs are stored in Standard Tier before aging into the Flex Tier or being...
    type: int

  tags:
    description:
      - >-
        A list of tags associated with the index. Tags must be in key:value format.
    type: list
    elements: str

extends_documentation_fragment:
  - stevefulme1.datadog.auth
"""

EXAMPLES = r"""

- name: Create a config_indexe
  stevefulme1.datadog.config_indexe:

    filter: "example_filter"

    name: "example_name"

    state: present
  # API: POST /api/v1/logs/config/indexes

- name: Update a config_indexe
  stevefulme1.datadog.config_indexe:
    id: "existing_id"

    daily_limit: "updated_daily_limit"

    daily_limit_reset: "updated_daily_limit_reset"

    daily_limit_warning_threshold_percentage: "updated_daily_limit_warning_threshold_percentage"

    disable_daily_limit: "updated_disable_daily_limit"

    exclusion_filters: "updated_exclusion_filters"

    is_rate_limited: "updated_is_rate_limited"

    num_flex_logs_retention_days: "updated_num_flex_logs_retention_days"

    num_retention_days: "updated_num_retention_days"

    tags: "updated_tags"

    state: present
  # API:

- name: Delete a config_indexe
  stevefulme1.datadog.config_indexe:
    id: "existing_id"
    state: absent
  # API: DELETE /api/v1/logs/config/indexes/{name}

"""

RETURN = r"""

daily_limit:
  description: >-
    The number of log events you can send in this index per day before you are rate-limited.
  returned: success
  type: int

daily_limit_reset:
  description: >-
    Object containing options to override the default daily limit reset time.
  returned: success
  type: dict

daily_limit_warning_threshold_percentage:
  description: >-
    A percentage threshold of the daily quota at which a Datadog warning event is generated.
  returned: success
  type: float

exclusion_filters:
  description: >-
    An array of exclusion objects. The logs are tested against the query of each filter, following...
  returned: success
  type: list

filter:
  description: >-
    Filter for logs.
  returned: success
  type: dict

is_rate_limited:
  description: >-
    A boolean stating if the index is rate limited, meaning more logs than the daily limit have been...
  returned: success
  type: bool

name:
  description: >-
    The name of the index.
  returned: success
  type: str

num_flex_logs_retention_days:
  description: >-
    The total number of days logs are stored in Standard and Flex Tier before being deleted from the...
  returned: success
  type: int

num_retention_days:
  description: >-
    The number of days logs are stored in Standard Tier before aging into the Flex Tier or being...
  returned: success
  type: int

tags:
  description: >-
    A list of tags associated with the index. Tags must be in key:value format.
  returned: success
  type: list

"""


def get_current_state(client, module):
    """Retrieve the current state of the config_indexe via GET."""

    # No single-resource GET endpoint; fall back to list + filter
    identifier = module.params.get("id")

    name = module.params.get("name")
    search_key = "name"
    search_value = name if identifier is None else identifier

    if search_value is None:
        return None
    try:
        items = client.get("/api/v1/logs/config/indexes")
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

    if module.params.get("filter") is not None:
        payload["filter"] = module.params["filter"]

    if module.params.get("name") is not None:
        payload["name"] = module.params["name"]

    if module.params.get("daily_limit") is not None:
        payload["daily_limit"] = module.params["daily_limit"]

    if module.params.get("daily_limit_reset") is not None:
        payload["daily_limit_reset"] = module.params["daily_limit_reset"]

    if module.params.get("daily_limit_warning_threshold_percentage") is not None:
        payload["daily_limit_warning_threshold_percentage"] = module.params["daily_limit_warning_threshold_percentage"]

    if module.params.get("disable_daily_limit") is not None:
        payload["disable_daily_limit"] = module.params["disable_daily_limit"]

    if module.params.get("exclusion_filters") is not None:
        payload["exclusion_filters"] = module.params["exclusion_filters"]

    if module.params.get("is_rate_limited") is not None:
        payload["is_rate_limited"] = module.params["is_rate_limited"]

    if module.params.get("num_flex_logs_retention_days") is not None:
        payload["num_flex_logs_retention_days"] = module.params["num_flex_logs_retention_days"]

    if module.params.get("num_retention_days") is not None:
        payload["num_retention_days"] = module.params["num_retention_days"]

    if module.params.get("tags") is not None:
        payload["tags"] = module.params["tags"]

    return payload


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            filter=dict(
                type="dict",

                required=True,

            ),

            name=dict(
                type="str",

                required=True,

            ),

            daily_limit=dict(
                type="int",

            ),

            daily_limit_reset=dict(
                type="dict",

            ),

            daily_limit_warning_threshold_percentage=dict(
                type="float",

            ),

            disable_daily_limit=dict(
                type="bool",

            ),

            exclusion_filters=dict(
                type="list", elements="str",

            ),

            is_rate_limited=dict(
                type="bool",

            ),

            num_flex_logs_retention_days=dict(
                type="int",

            ),

            num_retention_days=dict(
                type="int",

            ),

            tags=dict(
                type="list", elements="str",

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
                        "/api/v1/logs/config/indexes",
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
                    path = "/api/v1/logs/config/indexes/{name}".replace(
                        "{id}", str(identifier)
                    )
                    response = client.put(
                        path,
                        data=desired,
                    )
                    result.update(response if isinstance(response, dict) else {})

            else:
                # Resource exists and is up-to-date

                result["daily_limit"] = current.get("daily_limit")

                result["daily_limit_reset"] = current.get("daily_limit_reset")

                result["daily_limit_warning_threshold_percentage"] = current.get(
                    "daily_limit_warning_threshold_percentage"
                )

                result["exclusion_filters"] = current.get("exclusion_filters")

                result["filter"] = current.get("filter")

                result["is_rate_limited"] = current.get("is_rate_limited")

                result["name"] = current.get("name")

                result["num_flex_logs_retention_days"] = current.get("num_flex_logs_retention_days")

                result["num_retention_days"] = current.get("num_retention_days")

                result["tags"] = current.get("tags")

        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "/api/v1/logs/config/indexes/{name}".replace(
                        "{id}", str(identifier)
                    )
                    client.delete(path)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
