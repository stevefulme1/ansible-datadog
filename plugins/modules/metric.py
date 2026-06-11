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
module: metric
short_description: Manage metrics
version_added: "1.0.0"
description:
  - Create, update, and delete metric resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  state:
    description:
      - Desired state of the metric resource.
    type: str
    choices: ['present', 'absent']
    default: present

  description:
    description:
      - >-
        Metric description.
    type: str

  integration:
    description:
      - >-
        Name of the integration that sent the metric if applicable.
    type: str

  per_unit:
    description:
      - >-
        Per unit of the metric such as second in bytes per second.
    type: str

  short_name:
    description:
      - >-
        A more human-readable and abbreviated version of the metric name.
    type: str

  statsd_interval:
    description:
      - >-
        StatsD flush interval of the metric in seconds if applicable.
    type: int

  type:
    description:
      - >-
        Metric type such as gauge or rate.
    type: str

  unit:
    description:
      - >-
        Primary unit of the metric such as byte or operation.
    type: str

extends_documentation_fragment:
  - stevefulme1.datadog.auth
"""

EXAMPLES = r"""

- name: Update a metric
  stevefulme1.datadog.metric:
    id: "existing_id"

    description: "updated_description"

    integration: "updated_integration"

    per_unit: "updated_per_unit"

    short_name: "updated_short_name"

    statsd_interval: "updated_statsd_interval"

    type: "updated_type"

    unit: "updated_unit"

    state: present
  # API:

"""

RETURN = r"""

description:
  description: >-
    Metric description.
  returned: success
  type: str

integration:
  description: >-
    Name of the integration that sent the metric if applicable.
  returned: success
  type: str

per_unit:
  description: >-
    Per unit of the metric such as second in bytes per second.
  returned: success
  type: str

short_name:
  description: >-
    A more human-readable and abbreviated version of the metric name.
  returned: success
  type: str

statsd_interval:
  description: >-
    StatsD flush interval of the metric in seconds if applicable.
  returned: success
  type: int

type:
  description: >-
    Metric type such as gauge or rate.
  returned: success
  type: str

unit:
  description: >-
    Primary unit of the metric such as byte or operation.
  returned: success
  type: str

"""


def get_current_state(client, module):
    """Retrieve the current state of the metric via GET."""

    # No single-resource GET endpoint; fall back to list + filter
    identifier = module.params.get("id")

    search_key = "id"
    search_value = identifier

    if search_value is None:
        return None
    try:
        items = client.get("/api/v1/metrics")
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

    if module.params.get("description") is not None:
        payload["description"] = module.params["description"]

    if module.params.get("integration") is not None:
        payload["integration"] = module.params["integration"]

    if module.params.get("per_unit") is not None:
        payload["per_unit"] = module.params["per_unit"]

    if module.params.get("short_name") is not None:
        payload["short_name"] = module.params["short_name"]

    if module.params.get("statsd_interval") is not None:
        payload["statsd_interval"] = module.params["statsd_interval"]

    if module.params.get("type") is not None:
        payload["type"] = module.params["type"]

    if module.params.get("unit") is not None:
        payload["unit"] = module.params["unit"]

    return payload


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            description=dict(
                type="str",

            ),

            integration=dict(
                type="str",

            ),

            per_unit=dict(
                type="str",

            ),

            short_name=dict(
                type="str",

            ),

            statsd_interval=dict(
                type="int",

            ),

            type=dict(
                type="str",

            ),

            unit=dict(
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
                    # Metrics are auto-created when data is submitted.
                    # This module can only update metric metadata.
                    name = module.params.get("name")
                    if name:
                        response = client.put(
                            "/api/v1/metrics/{0}".format(name),
                            data=desired,
                        )
                        result.update(response if isinstance(response, dict) else {})
                    else:
                        module.fail_json(msg="name is required to update metric metadata")

            elif needs_update(current, desired):
                # Resource exists but needs updating
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = dict(current, **{k: v for k, v in desired.items() if v is not None})

                if not module.check_mode:

                    name = current.get("name", module.params.get("name"))
                    path = "/api/v1/metrics/{0}".format(name)
                    response = client.put(
                        path,
                        data=desired,
                    )
                    result.update(response if isinstance(response, dict) else {})

            else:
                # Resource exists and is up-to-date

                result["description"] = current.get("description")

                result["integration"] = current.get("integration")

                result["per_unit"] = current.get("per_unit")

                result["short_name"] = current.get("short_name")

                result["statsd_interval"] = current.get("statsd_interval")

                result["type"] = current.get("type")

                result["unit"] = current.get("unit")

        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:
                    module.fail_json(msg="Datadog metrics cannot be deleted via API. "
                                         "Metrics exist as long as data is submitted.")

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
