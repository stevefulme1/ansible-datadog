# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability within this collection, please send an email to sfulmer@redhat.com. All security vulnerabilities will be promptly addressed.

Please include the following information:

- Type of vulnerability
- Full path of the affected source file(s)
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the vulnerability

## Security Best Practices

When using this collection:

1. **Protect API Credentials**: Never commit Datadog API or Application keys to version control. Use Ansible Vault, environment variables, or external secret management systems.

2. **Use HTTPS**: All API communication uses HTTPS by default. Do not disable SSL verification in production.

3. **Least Privilege**: Use Datadog Application keys with minimal required permissions for your automation tasks.

4. **Regular Updates**: Keep the collection and its dependencies updated to receive security patches.

5. **EDA Webhook Security**: When using the EDA webhook event source, ensure:
   - The webhook endpoint is behind authentication/firewall
   - Webhooks are validated using Datadog's signature verification
   - Network traffic is encrypted (TLS/SSL)

## Known Security Considerations

- API keys are passed to modules as parameters. Ensure these are properly secured using Ansible Vault or similar mechanisms.
- The EDA webhook event source listens on a network port. Implement appropriate network security controls.
