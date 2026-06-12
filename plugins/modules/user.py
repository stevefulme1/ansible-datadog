#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Auto-generated from Datadog API spec
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: user
short_description: Manage users
version_added: "1.0.0"
description:
  - Create, update, and delete user resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  state:
    description:
      - Desired state of the user resource.
    type: str
    choices: ['present', 'absent']
    default: present

  access_role:
    description:
      - >-
        The access role of the user. Options are st (standard user), adm (admin user), or ro (read-only user).
    type: str

    choices: ["st", "adm", "ro", "ERROR"]

  disabled:
    description:
      - >-
        The new disabled status of the user.
    type: bool

  email:
    description:
      - >-
        The new email of the user.
    type: str

  handle:
    description:
      - >-
        The user handle, must be a valid email.
    type: str

  icon:
    description:
      - >-
        Gravatar icon associated to the user.
    type: str

  name:
    description:
      - >-
        The name of the user.
    type: str

  verified:
    description:
      - >-
        Whether or not the user logged in Datadog at least once.
    type: bool

extends_documentation_fragment:
  - stevefulme1.datadog.auth
"""

EXAMPLES = r"""

- name: Create a user
  stevefulme1.datadog.user:

    state: present
  # API: POST /api/v1/user

- name: Update a user
  stevefulme1.datadog.user:
    id: "existing_id"

    access_role: "updated_access_role"

    disabled: "updated_disabled"

    email: "updated_email"

    handle: "updated_handle"

    icon: "updated_icon"

    name: "updated_name"

    verified: "updated_verified"

    state: present
  # API:

- name: Delete a user
  stevefulme1.datadog.user:
    id: "existing_id"
    state: absent
  # API: DELETE /api/v1/user/{user_handle}

"""

RETURN = r"""

user:
  description: >-
    Create, edit, and disable users.
  returned: success
  type: dict

"""

from ansible_collections.stevefulme1.datadog.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)
from ansible.module_utils.basic import AnsibleModule


def get_current_state(client, module):
    """Retrieve the current state of the user via GET."""

    # No single-resource GET endpoint; fall back to list + filter
    identifier = module.params.get("id")

    search_key = "id"
    search_value = identifier

    if search_value is None:
        return None
    try:
        items = client.get("/api/v1/user")
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

    if module.params.get("access_role") is not None:
        payload["access_role"] = module.params["access_role"]

    if module.params.get("disabled") is not None:
        payload["disabled"] = module.params["disabled"]

    if module.params.get("email") is not None:
        payload["email"] = module.params["email"]

    if module.params.get("handle") is not None:
        payload["handle"] = module.params["handle"]

    if module.params.get("icon") is not None:
        payload["icon"] = module.params["icon"]

    if module.params.get("name") is not None:
        payload["name"] = module.params["name"]

    if module.params.get("verified") is not None:
        payload["verified"] = module.params["verified"]

    return payload


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            access_role=dict(
                type="str",

                choices=['st', 'adm', 'ro', 'ERROR'],

            ),

            disabled=dict(
                type="bool",

            ),

            email=dict(
                type="str",

            ),

            handle=dict(
                type="str",

            ),

            icon=dict(
                type="str",

            ),

            name=dict(
                type="str",

            ),

            verified=dict(
                type="bool",

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
                        "/api/v1/user",
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
                    path = "/api/v2/users/{id}".replace(
                        "{id}", str(identifier)
                    )
                    response = client.put(
                        path,
                        data=desired,
                    )
                    result.update(response if isinstance(response, dict) else {})

            else:
                # Resource exists and is up-to-date

                result["user"] = current.get("user")

        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "/api/v1/user/{user_handle}".replace(
                        "{id}", str(identifier)
                    )
                    client.delete(path)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
