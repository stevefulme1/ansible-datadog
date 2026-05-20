#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Auto-generated from Datadog API spec
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: synthetic_variable
short_description: Manage synthetics
version_added: "1.0.0"
description:
  - Create, update, and delete synthetic_variable resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  state:
    description:
      - Desired state of the synthetic_variable resource.
    type: str
    choices: ['present', 'absent']
    default: present

  description:
    description:
      - >-
        Description of the global variable.
    type: str

    required: true





  name:
    description:
      - >-
        Name of the global variable. Unique across Synthetic global variables.
    type: str

    required: true





  tags:
    description:
      - >-
        Tags of the global variable.
    type: list
    elements: str

    required: true





  attributes:
    description:
      - >-
        Attributes of the global variable.
    type: dict





  id:
    description:
      - >-
        Unique identifier of the global variable.
    type: str





  is_fido:
    description:
      - >-
        Determines if the global variable is a FIDO variable.
    type: bool





  is_totp:
    description:
      - >-
        Determines if the global variable is a TOTP/MFA variable.
    type: bool





  parse_test_options:
    description:
      - >-
        Parser options to use for retrieving a Synthetic global variable from a Synthetic test. Used in...
    type: dict





  parse_test_public_id:
    description:
      - >-
        A Synthetic test ID to use as a test to generate the variable value.
    type: str





  value:
    description:
      - >-
        Value of the global variable.
    type: dict





extends_documentation_fragment:
  - stevefulme1.datadog.auth
"""

EXAMPLES = r"""

- name: Create a synthetic_variable
  stevefulme1.datadog.synthetic_variable:


    description: "example_description"



    name: "example_name"



    tags: "example_tags"
















    state: present
  # API: POST /api/v1/synthetics/variables



- name: Update a synthetic_variable
  stevefulme1.datadog.synthetic_variable:
    id: "existing_id"








    attributes: "updated_attributes"





    is_fido: "updated_is_fido"



    is_totp: "updated_is_totp"



    parse_test_options: "updated_parse_test_options"



    parse_test_public_id: "updated_parse_test_public_id"



    value: "updated_value"


    state: present
  # API:  



- name: Delete a synthetic_variable
  stevefulme1.datadog.synthetic_variable:
    id: "existing_id"
    state: absent
  # API: DELETE /api/v1/synthetics/variables/{variable_id}

"""

RETURN = r"""

attributes:
  description: >-
    Attributes of the global variable.
  returned: success
  type: dict


description:
  description: >-
    Description of the global variable.
  returned: success
  type: str


id:
  description: >-
    Unique identifier of the global variable.
  returned: success
  type: str


is_fido:
  description: >-
    Determines if the global variable is a FIDO variable.
  returned: success
  type: bool


is_totp:
  description: >-
    Determines if the global variable is a TOTP/MFA variable.
  returned: success
  type: bool


name:
  description: >-
    Name of the global variable. Unique across Synthetic global variables.
  returned: success
  type: str


parse_test_options:
  description: >-
    Parser options to use for retrieving a Synthetic global variable from a Synthetic test. Used in...
  returned: success
  type: dict


parse_test_public_id:
  description: >-
    A Synthetic test ID to use as a test to generate the variable value.
  returned: success
  type: str


tags:
  description: >-
    Tags of the global variable.
  returned: success
  type: list


value:
  description: >-
    Value of the global variable.
  returned: success
  type: dict


"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.datadog.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)


def get_current_state(client, module):
    """Retrieve the current state of the synthetic_variable via GET."""

    # No single-resource GET endpoint; fall back to list + filter
    identifier = module.params.get("id")

    name = module.params.get("name")
    search_key = "name"
    search_value = name if identifier is None else identifier

    if search_value is None:
        return None
    try:
        items = client.get("/api/v1/synthetics/variables")
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

    if module.params.get("name") is not None:
        payload["name"] = module.params["name"]

    if module.params.get("tags") is not None:
        payload["tags"] = module.params["tags"]

    if module.params.get("attributes") is not None:
        payload["attributes"] = module.params["attributes"]

    if module.params.get("id") is not None:
        payload["id"] = module.params["id"]

    if module.params.get("is_fido") is not None:
        payload["is_fido"] = module.params["is_fido"]

    if module.params.get("is_totp") is not None:
        payload["is_totp"] = module.params["is_totp"]

    if module.params.get("parse_test_options") is not None:
        payload["parse_test_options"] = module.params["parse_test_options"]

    if module.params.get("parse_test_public_id") is not None:
        payload["parse_test_public_id"] = module.params["parse_test_public_id"]

    if module.params.get("value") is not None:
        payload["value"] = module.params["value"]

    return payload


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            description=dict(
                type="str",

                required=True,





            ),

            name=dict(
                type="str",

                required=True,





            ),

            tags=dict(
                type="list", elements="str",

                required=True,





            ),

            attributes=dict(
                type="dict",





            ),

            id=dict(
                type="str",





            ),

            is_fido=dict(
                type="bool",





            ),

            is_totp=dict(
                type="bool",





            ),

            parse_test_options=dict(
                type="dict",





            ),

            parse_test_public_id=dict(
                type="str",





            ),

            value=dict(
                type="dict",





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
                        "/api/v1/synthetics/variables",
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
                    path = "/api/v1/synthetics/variables/{id}".replace(
                        "{id}", str(identifier)
                    )
                    response = client.put(
                        path,
                        data=desired,
                    )
                    result.update(response if isinstance(response, dict) else {})


            else:
                # Resource exists and is up-to-date

                result["attributes"] = current.get("attributes")

                result["description"] = current.get("description")

                result["id"] = current.get("id")

                result["is_fido"] = current.get("is_fido")

                result["is_totp"] = current.get("is_totp")

                result["name"] = current.get("name")

                result["parse_test_options"] = current.get("parse_test_options")

                result["parse_test_public_id"] = current.get("parse_test_public_id")

                result["tags"] = current.get("tags")

                result["value"] = current.get("value")


        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "/api/v1/synthetics/variables/{variable_id}".replace(
                        "{id}", str(identifier)
                    )
                    client.delete(path)


    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
