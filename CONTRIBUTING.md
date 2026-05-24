# Contributing to Cryptora

Thank you for your interest in improving Cryptora.

## Engineering Standards
- Preserve DDD and Clean Architecture boundaries.
- Keep domain layer framework-agnostic.
- Add tests for all functional changes.
- Avoid introducing plaintext secret persistence.

## Development Workflow
1. Create a feature branch.
2. Implement changes with clear, focused commits.
3. Run local quality checks.
4. Submit PR with architecture/security rationale.

## Required Checks
Run before opening PR:
```bash
pytest -q
```

## Code Review Expectations
PR descriptions should include:
- what changed
- why it changed
- security implications
- test evidence

## Security-Sensitive Changes
For changes in crypto, key derivation, auth, or persistence of secrets:
- include threat model notes
- include regression tests
- request focused security review

## Style and Quality
- Follow PEP 8.
- Prefer explicit naming over clever abstractions.
- Keep functions cohesive and side effects explicit.

## Issue Reporting
Use issues for bugs and improvements. For vulnerabilities, follow [SECURITY.md](./SECURITY.md).
