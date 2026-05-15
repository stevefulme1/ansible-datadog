# Contributing to stevefulme1.datadog

Thank you for your interest in contributing to the Datadog Ansible collection!

## How to Contribute

1. **Fork the Repository**: Create your own fork of the project
2. **Create a Branch**: Make your changes in a new git branch
3. **Make Your Changes**: Follow the coding standards below
4. **Test Your Changes**: Ensure tests pass
5. **Submit a Pull Request**: Open a PR with a clear description

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ansible-datadog.git
cd ansible-datadog

# Install dependencies
pip install -r requirements.txt
pip install -r tests/requirements.txt

# Run tests
ansible-test sanity --docker default
pytest tests/unit -v
```

## Coding Standards

- Follow [Ansible module conventions](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html)
- Use `ansible-lint` to validate playbooks and roles
- Add docstrings to all modules following Ansible documentation standards
- Include examples in module documentation
- Support check mode where applicable
- Return meaningful changed/failed status

## Module Development Guidelines

### Required Components

Every new module should include:

1. **DOCUMENTATION**: YAML documentation block with description, options, examples
2. **EXAMPLES**: At least 3 usage examples
3. **RETURN**: Document all return values
4. **Check Mode**: Support `--check` mode
5. **Idempotency**: Module should be idempotent
6. **Error Handling**: Proper exception handling with meaningful messages

### Module Template

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Steve Fulmer <sfulmer@redhat.com>
# Apache License 2.0 (see LICENSE or http://www.apache.org/licenses/LICENSE-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: datadog_example
short_description: Manage Datadog resources
description:
  - Create, update, or delete Datadog resources
  - Retrieve information about resources
options:
  name:
    description: Resource name
    type: str
    required: true
  state:
    description: Desired state
    type: str
    choices: [present, absent]
    default: present
extends_documentation_fragment:
  - stevefulme1.datadog.datadog_auth
'''

EXAMPLES = r'''
- name: Create resource
  stevefulme1.datadog.datadog_example:
    api_key: "{{ api_key }}"
    app_key: "{{ app_key }}"
    name: "my-resource"
    state: present
'''

RETURN = r'''
resource:
  description: Resource details
  returned: success
  type: dict
'''
```

## Testing Requirements

### Unit Tests

- Add unit tests for all new modules
- Test success and failure scenarios
- Mock API calls using `unittest.mock`
- Aim for >80% code coverage

### Integration Tests

- Provide integration test stubs in `tests/integration/targets/`
- Document manual testing procedures if automated integration is not possible

### Sanity Tests

All PRs must pass:

```bash
ansible-test sanity --docker default -v
```

## Pull Request Process

1. Update the CHANGELOG.md with details of changes
2. Update documentation if adding/changing functionality
3. Ensure all tests pass
4. Request review from maintainers
5. Address any review feedback

## Code of Conduct

This project follows the Contributor Covenant Code of Conduct. Please read CODE_OF_CONDUCT.md.

## Questions?

Open an issue or contact the maintainers at sfulmer@redhat.com.
