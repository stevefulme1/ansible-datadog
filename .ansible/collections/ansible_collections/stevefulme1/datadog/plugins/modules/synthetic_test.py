#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Auto-generated from Datadog API spec
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: synthetic_test
short_description: Manage synthetics
version_added: "1.0.0"
description:
  - Create, update, and delete synthetic_test resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  state:
    description:
      - Desired state of the synthetic_test resource.
    type: str
    choices: ['present', 'absent']
    default: present

  data:
    description:
      - >-
        Array of JSON Patch operations to perform on the test
    type: list
    elements: str





extends_documentation_fragment:
  - stevefulme1.datadog.auth
"""

EXAMPLES = r"""


- name: Update a synthetic_test
  stevefulme1.datadog.synthetic_test:
    monitor_id: "existing_id"


    data: "updated_data"


    state: present
  # API:  



"""

RETURN = r"""

config:
  description: >-
    Configuration object for a Synthetic test.
  returned: success
  type: dict


creator:
  description: >-
    Object describing the creator of the shared element.
  returned: success
  type: dict


locations:
  description: >-
    Array of locations used to run the test.
  returned: success
  type: list


message:
  description: >-
    Notification message associated with the test.
  returned: success
  type: str


monitor_id:
  description: >-
    The associated monitor ID.
  returned: success
  type: int


name:
  description: >-
    Name of the test.
  returned: success
  type: str


options:
  description: >-
    Object describing the extra options for a Synthetic test.
  returned: success
  type: dict


public_id:
  description: >-
    The test public ID.
  returned: success
  type: str


status:
  description: >-
    Define whether you want to start (live) or pause (paused) a Synthetic test.
  returned: success
  type: str


subtype:
  description: >-
    The subtype of the Synthetic API test, http, ssl, tcp, dns, icmp, udp, websocket, grpc or multi.
  returned: success
  type: str


tags:
  description: >-
    Array of tags attached to the test.
  returned: success
  type: list


type:
  description: >-
    Type of the Synthetic test.
  returned: success
  type: str


"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.datadog.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)


def get_current_state(client, module):
    """Retrieve the current state of the synthetic_test via GET."""

    # No single-resource GET endpoint; fall back to list + filter
    identifier = module.params.get("monitor_id")

    name = module.params.get("name")
    search_key = "name"
    search_value = name if identifier is None else identifier

    if search_value is None:
        return None
    try:
        items = client.get("/api/v1/synthetics/tests")
        if isinstance(items, dict):
            items = items.get("results", items.get("data", items.get("items", [])))
        for item in items:
            if str(item.get(search_key)) == str(search_value):
                return item
            if str(item.get("monitor_id")) == str(search_value):
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

    return payload


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            data=dict(
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
                        "/api/v1/synthetics/tests",
                        data=desired,
                    )
                    result.update(response if isinstance(response, dict) else {})


            elif needs_update(current, desired):
                # Resource exists but needs updating
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = dict(current, **{k: v for k, v in desired.items() if v is not None})

                if not module.check_mode:

                    identifier = current.get("monitor_id")
                    path = "/api/v1/synthetics/tests/{public_id}".replace(
                        "{monitor_id}", str(identifier)
                    )
                    response = client.put(
                        path,
                        data=desired,
                    )
                    result.update(response if isinstance(response, dict) else {})


            else:
                # Resource exists and is up-to-date

                result["config"] = current.get("config")

                result["creator"] = current.get("creator")

                result["locations"] = current.get("locations")

                result["message"] = current.get("message")

                result["monitor_id"] = current.get("monitor_id")

                result["name"] = current.get("name")

                result["options"] = current.get("options")

                result["public_id"] = current.get("public_id")

                result["status"] = current.get("status")

                result["subtype"] = current.get("subtype")

                result["tags"] = current.get("tags")

                result["type"] = current.get("type")


        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    response = client.post(
                        "/api/v1/synthetics/tests",
                        data=desired,
                    )
                    result.update(response if isinstance(response, dict) else {})


    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
