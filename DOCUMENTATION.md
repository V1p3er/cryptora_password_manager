# Cryptora Technical Documentation

## 1. Overview
Cryptora is a layered password manager backend using DDD and Clean Architecture. The project isolates core business rules from cryptographic and persistence implementation details to maximize correctness, testability, and replaceability.

## 2. Layered Design

### Domain Layer
The domain layer contains:
- value objects for validated data boundaries (`UserId`, `Username`, `DomainName`, `EncryptedValue`, etc.)
- entities and aggregate behavior (`User`, `Vault`, `VaultItem`)
- repository contracts (`UserRepository`, `VaultRepository`)
- service abstractions and domain utility services

Why this design:
- keeps invariants close to data
- prevents primitive obsession
- avoids framework leakage into business rules

### Application Layer
The application layer orchestrates use-cases:
- `CreateVaultService`
- `UnlockVaultService` / `LockVaultService`
- `AddCredentialService`
- `ListCredentialsService`
- `GetCredentialService`
- `UpdateCredentialService`
- `RemoveCredentialService`

Why this design:
- one place for workflow policies and error mapping
- domain remains pure and composable
- interface layer stays thin

### Infrastructure Layer
Infrastructure implements technical adapters:
- crypto: Argon2 key derivation and AES-GCM encryption
- security: password hash/verify adapter, integrity checker, audit logger
- persistence: file-based repository implementations for domain contracts
- config: environment-backed settings

Why this design:
- swappable adapters without touching domain logic
- explicit dependency inversion
- deterministic integration and e2e testing

### Interface Layer
The CLI interface provides interactive operational flows for:
- registration
- login
- vault creation/unlock/lock
- credential CRUD

CLI UX characteristics:
- looped menu
- `0` exit
- retry on invalid input with explicit reason
- `cancel` option in operations

## 3. Security Model

### Password Handling
- Master passwords are validated by domain value object rules.
- Password hashes are generated/verified with Argon2.
- Raw master passwords are not persisted.

### Data Encryption
- Credential secrets are encrypted via AES-GCM.
- Encryption keys are derived from master password + user-derived salt using Argon2.
- Repositories store encrypted values only.

### Data Integrity and Auditability
- HMAC-based integrity checker utility is provided for signed payload verification use cases.
- Audit logger utility provides structured event logging seam.

## 4. Persistence Strategy
Current persistence implementation is file-based JSON repositories implementing domain contracts.

Benefits:
- simple local bootstrap
- deterministic tests
- contract-first path for future database adapters

Planned extension path:
- add SQL database adapter behind same repository interfaces
- maintain all application/domain behavior unchanged

## 5. Testing Strategy

### Unit Tests
- Domain invariants and behaviors
- Application use-case behavior and failure modes
- Infrastructure adapter correctness

### Integration Tests
- Cross-layer behavior with real adapters

### End-to-End Test
- `tests/e2e/full_test.py` verifies full application flow:
- user creation and password validation
- vault creation
- add/list/get/update/remove credential operations
- lock/unlock behavior
- negative-path validation (invalid password, locked vault, missing credential)

## 6. Why This Implementation Style
- High confidence via clear boundaries and layered tests
- Security-sensitive logic isolated and explicit
- Lower change risk: infra details can evolve independently
- Better long-term maintainability in team environments

## 7. Operational Notes
- Run tests with `pytest -q`
- Run CLI app via `python main.py`
- Configure storage path with environment variable `CRYPTORA_STORAGE_FILE_PATH`

## 8. Trade-offs and Current Scope
- Current storage is file-based; good for architecture validation, not yet optimized for distributed multi-process writes.
- API interface is scaffolded but CLI is the active interface implementation.
- Some utilities (integrity checker, audit logger) are provided as seams and can be expanded by deployment needs.
