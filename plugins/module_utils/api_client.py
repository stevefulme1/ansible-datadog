# -*- coding: utf-8 -*-
# Copyright 2026 Steve Fulmer
# Apache-2.0 (see LICENSE)

"""Datadog API client using real v1/v2 endpoints."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

IMPORT_ERRORS = []
try:
    import requests
    HAS_REQUESTS = True
except ImportError as e:
    HAS_REQUESTS = False
    IMPORT_ERRORS.append(e)


# Datadog API endpoint mapping (real v1 endpoints)
RESOURCE_ENDPOINTS = {
    "monitor": {
        "base": "/api/v1/monitor",
        "item": "/api/v1/monitor/{id}",
        "id_field": "id",
        "list_key": None,  # returns list directly
        "search": "/api/v1/monitor/search",
    },
    "dashboard": {
        "base": "/api/v1/dashboard",
        "item": "/api/v1/dashboard/{id}",
        "id_field": "id",
        "list_key": "dashboards",
        "search": None,
    },
    "synthetic": {
        "base": "/api/v1/synthetics/tests",
        "item": "/api/v1/synthetics/tests/{id}",
        "id_field": "public_id",
        "list_key": "tests",
        "search": None,
    },
}


class ApiClient:
    """REST API client for Datadog using real v1 API endpoints."""

    def __init__(self, module):
        self.module = module
        self.host = module.params["host"]
        self.validate_certs = module.params.get("validate_certs", True)
        self.session = requests.Session()
        self.session.verify = self.validate_certs
        self._authenticate()

    def _authenticate(self):
        api_key = self.module.params.get("api_key")
        app_key = self.module.params.get("app_key", "")
        if api_key:
            self.session.headers["DD-API-KEY"] = api_key
            if app_key:
                self.session.headers["DD-APPLICATION-KEY"] = app_key
        self.session.headers["Content-Type"] = "application/json"

    def _url(self, path):
        return "https://{host}{path}".format(host=self.host, path=path)

    def _endpoint(self, resource_type):
        ep = RESOURCE_ENDPOINTS.get(resource_type)
        if not ep:
            self.module.fail_json(
                msg="Unknown resource type: {0}".format(resource_type)
            )
        return ep

    def get(self, resource_type, resource_id):
        """GET a single resource by ID. Returns None if 404."""
        ep = self._endpoint(resource_type)
        url = self._url(ep["item"].format(id=resource_id))
        resp = self.session.get(url)
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        return resp.json()

    def list(self, resource_type, params=None):
        """List resources, optionally filtered."""
        ep = self._endpoint(resource_type)
        url = self._url(ep["base"])
        resp = self.session.get(url, params=params or {})
        resp.raise_for_status()
        data = resp.json()
        if ep["list_key"]:
            return data.get(ep["list_key"], [])
        if isinstance(data, list):
            return data
        return data.get("data", [])

    def find_by_name(self, resource_type, name):
        """Find a resource by name. Returns first match or None."""
        items = self.list(resource_type)
        for item in items:
            item_name = item.get("name") or item.get("title", "")
            if item_name == name:
                return item
        return None

    def create(self, resource_type, payload):
        """POST to create a new resource."""
        ep = self._endpoint(resource_type)
        url = self._url(ep["base"])
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def update(self, resource_type, resource_id, payload):
        """PUT to update an existing resource."""
        ep = self._endpoint(resource_type)
        url = self._url(ep["item"].format(id=resource_id))
        resp = self.session.put(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def delete(self, resource_type, resource_id):
        """DELETE a resource. Silently succeeds if already gone (404)."""
        ep = self._endpoint(resource_type)
        url = self._url(ep["item"].format(id=resource_id))
        resp = self.session.delete(url)
        if resp.status_code == 404:
            return
        resp.raise_for_status()
