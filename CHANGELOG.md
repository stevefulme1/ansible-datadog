# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0]

### Added

- 50 modules covering full Datadog platform API
- CRUD + info module for every resource type
- EDA source plugins for event-driven automation
- Unit tests and CI pipeline

## [1.0.0-initial] - 2026-05-15

### Added

- Initial release of stevefulme1.datadog collection
- Monitor management modules (`datadog_monitor`, `datadog_monitor_info`)
- Dashboard management modules (`datadog_dashboard`, `datadog_dashboard_info`)
- SLO management modules (`datadog_slo`, `datadog_slo_info`)
- Synthetic test management modules (`datadog_synthetic`, `datadog_synthetic_info`)
- Downtime management modules (`datadog_downtime`, `datadog_downtime_info`)
- EDA webhook event source for receiving Datadog monitor alerts
- EDA events event source for polling Datadog Events API
- Common module utilities for Datadog API authentication and requests
- Documentation fragments for consistent authentication parameters
- Example EDA rulebooks for alert remediation and SLO breach handling
- Unit tests for monitor module and API client
- CI pipeline for linting, sanity tests, and unit tests

[1.0.0]: https://github.com/stevefulme1/ansible-datadog/releases/tag/v1.0.0
