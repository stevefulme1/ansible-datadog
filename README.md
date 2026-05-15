# Ansible Collection - stevefulme1.datadog

Ansible collection for managing Datadog monitoring resources via the Datadog API. Includes modules for monitors, dashboards, SLOs, synthetic tests, downtimes, and EDA event sources for webhook and events integration.

## Description

This collection fills the gap left by the official `datadog.dd` collection, which only provides an agent installation role. The `stevefulme1.datadog` collection provides:

- **API Management Modules**: Create, update, delete, and query Datadog monitors, dashboards, SLOs, synthetic tests, and downtimes
- **EDA Event Sources**: Receive Datadog webhook alerts and poll the Events API for event-driven automation
- **Full CRUD Support**: All modules support check mode and return detailed state information

## Requirements

- Ansible >= 2.16.0
- Python >= 3.11
- `requests` library >= 2.25.0

## Installation

```bash
ansible-galaxy collection install stevefulme1.datadog
```

Or add to `requirements.yml`:

```yaml
---
collections:
  - name: stevefulme1.datadog
    version: ">=1.0.0"
```

## Authentication

All modules require Datadog API and Application keys. Set these via module parameters or environment variables:

```yaml
- name: Create a monitor
  stevefulme1.datadog.datadog_monitor:
    api_key: "{{ datadog_api_key }}"
    app_key: "{{ datadog_app_key }}"
    site: datadoghq.com  # or datadoghq.eu, us3.datadoghq.com, us5.datadoghq.com
    name: "High CPU Usage"
    type: metric alert
    query: "avg(last_5m):avg:system.cpu.user{*} > 90"
    state: present
```

Environment variables:
- `DD_API_KEY`: Datadog API key
- `DD_APP_KEY`: Datadog Application key
- `DD_SITE`: Datadog site (defaults to datadoghq.com)

## Modules

### Monitor Management
- `datadog_monitor`: Create, update, or delete monitors
- `datadog_monitor_info`: Retrieve monitor information

### Dashboard Management
- `datadog_dashboard`: Create, update, or delete dashboards
- `datadog_dashboard_info`: Retrieve dashboard information

### SLO Management
- `datadog_slo`: Create, update, or delete SLOs
- `datadog_slo_info`: Retrieve SLO information

### Synthetic Test Management
- `datadog_synthetic`: Create, update, or delete synthetic tests
- `datadog_synthetic_info`: Retrieve synthetic test information

### Downtime Management
- `datadog_downtime`: Create, update, or delete downtimes
- `datadog_downtime_info`: Retrieve downtime information

## EDA Event Sources

### Webhook Event Source

Receive Datadog monitor webhook alerts:

```yaml
---
- name: Handle Datadog alerts
  hosts: all
  sources:
    - stevefulme1.datadog.webhook:
        host: 0.0.0.0
        port: 8000
  rules:
    - name: Alert on critical monitors
      condition: event.alert_type == "error"
      action:
        run_playbook:
          name: remediate_critical_alert.yml
```

Configure Datadog monitors to send webhooks using `@webhook-<name>` in the monitor message.

### Events Event Source

Poll Datadog Events API:

```yaml
---
- name: Monitor Datadog events
  hosts: all
  sources:
    - stevefulme1.datadog.events:
        api_key: "{{ datadog_api_key }}"
        app_key: "{{ datadog_app_key }}"
        poll_interval: 60
        query: "status:error priority:high"
  rules:
    - name: Process high-priority errors
      condition: event.priority == "high"
      action:
        run_playbook:
          name: investigate_error.yml
```

## Example Playbooks

### Create a Metric Monitor

```yaml
---
- name: Manage Datadog monitors
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Create CPU monitor
      stevefulme1.datadog.datadog_monitor:
        api_key: "{{ lookup('env', 'DD_API_KEY') }}"
        app_key: "{{ lookup('env', 'DD_APP_KEY') }}"
        name: "High CPU Usage - {{ inventory_hostname }}"
        type: metric alert
        query: "avg(last_5m):avg:system.cpu.user{host:{{ inventory_hostname }}} > 90"
        message: |
          CPU usage is above 90% on {{ inventory_hostname }}
          @slack-alerts @pagerduty
        tags:
          - "env:production"
          - "team:platform"
        state: present
      register: monitor

    - name: Display monitor ID
      debug:
        msg: "Monitor created with ID {{ monitor.monitor.id }}"
```

### Create an SLO

```yaml
---
- name: Create API availability SLO
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Define 99.9% availability SLO
      stevefulme1.datadog.datadog_slo:
        api_key: "{{ lookup('env', 'DD_API_KEY') }}"
        app_key: "{{ lookup('env', 'DD_APP_KEY') }}"
        name: "API Availability"
        type: metric
        description: "99.9% availability for production API"
        query:
          numerator: "sum:api.requests.success{env:prod}.as_count()"
          denominator: "sum:api.requests.total{env:prod}.as_count()"
        thresholds:
          - timeframe: 7d
            target: 99.9
          - timeframe: 30d
            target: 99.9
        tags:
          - "service:api"
          - "env:production"
        state: present
```

## Testing

Run unit tests:

```bash
pytest tests/unit -v
```

Run sanity tests:

```bash
ansible-test sanity --docker default -v
```

## License

Apache-2.0

## Author Information

Steve Fulmer <sfulmer@redhat.com>
