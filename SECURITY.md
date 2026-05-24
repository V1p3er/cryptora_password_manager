# Security Policy

## Supported Versions
Only the latest release branch is supported for security fixes.

## Reporting a Vulnerability
Do not open public issues for vulnerabilities.

Send reports to: `contact@particelagency.com`

Please include:
- vulnerability type and impact
- affected components/files
- reproducible steps or proof of concept
- suggested remediation if available

## Response SLA
- Initial acknowledgement target: within 48 hours
- Triage and severity classification: within 5 business days
- Remediation timelines based on risk level and exploitability

## Scope
In-scope examples:
- cryptographic misuse or weakness
- broken authentication/authorization logic
- sensitive data leakage
- key management flaws
- tampering/integrity vulnerabilities

Out-of-scope examples:
- theoretical-only findings without practical impact
- dependency advisories with no exploitable path in Cryptora

## Disclosure Policy
Practice responsible disclosure. Allow maintainers reasonable time to investigate, patch, and publish remediation before public disclosure.

## Cryptographic Posture
Cryptora currently relies on:
- Argon2 for password hashing
- Argon2-based key derivation for data encryption keys
- AES-GCM for vault secret encryption

Any cryptography-related change must be reviewed with explicit threat and abuse-case analysis.
