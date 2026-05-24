# Cryptora

Cryptora is a security-focused password manager backend built with Domain-Driven Design (DDD) and Clean Architecture.

It is designed for:
- strict separation between business rules and technical implementation
- auditable crypto boundaries
- high testability across unit, integration, and end-to-end flows

## Core Principles
- `Domain first`: business invariants are enforced in value objects and entities.
- `Dependency inversion`: infrastructure implements domain contracts.
- `Security by design`: encryption, key derivation, and password verification are explicit components.
- `Test-driven confidence`: full stack is validated from domain to interface behavior.

## Architecture
```text
interfaces -> application -> domain
                    ^
             infrastructure
```

- `domain/`: entities, value objects, repository contracts, and domain services
- `application/`: use-case orchestration and application-level exceptions/DTOs
- `infrastructure/`: cryptography, persistence, config, and security adapters
- `interfaces/`: CLI and entrypoint wiring

## Runtime Features
- Argon2-based master password hashing and verification
- Argon2-based key derivation for data encryption keys
- AES-GCM encryption/decryption for credential secrets
- File-based persistence repositories implementing domain contracts
- Interactive CLI with:
- persistent loop menu
- `0` to exit
- retry-on-invalid-input with clear reason
- `cancel` support for all interactive operations

## Testing Strategy
- `tests/unit/`: isolated behavior of domain/application/infrastructure
- `tests/integration/`: cross-layer collaboration tests
- `tests/e2e/full_test.py`: full application flow test over real infrastructure adapters

Run all tests:
```bash
pytest -q
```

## Quick Start
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Run application:
```bash
python main.py
```

## Security Notes
- Never store plaintext secrets in persistent storage.
- Cryptora encrypts vault secrets before repository persistence.
- Report vulnerabilities privately via the security policy in [SECURITY.md](./SECURITY.md).

## Documentation
Detailed architecture and implementation rationale is available in [DOCUMENTATION.md](./DOCUMENTATION.md).
