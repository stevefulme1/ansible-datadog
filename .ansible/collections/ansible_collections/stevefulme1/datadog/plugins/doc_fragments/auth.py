# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer (@stevefulme1)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment:
    """Documentation fragment for stevefulme1.datadog authentication."""

    DOCUMENTATION = r"""
options:

  api_key:
    description:
      - The Datadog API key used for authentication.
      - Can also be set via the C(DATADOG_API_KEY) environment variable.
    type: str
    required: true

  application_key:
    description:
      - The Datadog application key for additional API access.
      - Can also be set via the C(DATADOG_APP_KEY) environment variable.
    type: str
    required: false

  api_url:
    description:
      - The base URL of the Datadog API.
      - Override for Datadog EU or government sites.
    type: str
    default: "https://api.datadoghq.com"
  validate_certs:
    description:
      - Whether to validate SSL/TLS certificates when connecting to the API.
    type: bool
    default: true
  request_timeout:
    description:
      - Timeout in seconds for API requests.
    type: int
    default: 30
"""
