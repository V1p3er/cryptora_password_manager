# Cryptora

Cryptora is a backend service for a password manager focused on **clear domain modeling and strong cryptographic boundaries**.  
The project follows a **Domain‑Driven Design (DDD) and Clean Architecture approach**, separating business rules from infrastructure and interface concerns.

The goal is to keep security‑critical logic explicit and testable while allowing infrastructure (database, API framework, crypto implementations) to change without affecting the core domain.

---

# Architecture Overview

Cryptora is organized into four primary layers:

```
interface → application → domain
                    ↑
              infrastructure
```

Each layer has a specific responsibility and strict dependency direction.

- **Domain** contains the core business rules and cryptographic concepts.
- **Application** orchestrates use‑cases.
- **Infrastructure** provides implementations for persistence and security primitives.
- **Interface** exposes the system through an API.

The domain layer does not depend on any external framework or infrastructure code.

---

# Project Structure

```
cryptora/

domain/
 ├── value_objects/
 ├── entities/
 ├── services/
 ├── repositories/
 └── exceptions.py

application/
 ├── use_cases/
 ├── dto/
 ├── services/
 └── exceptions.py

infrastructure/
 ├── persistence/
 ├── repositories/
 ├── security/
 ├── config/
 └── migrations/

interface/
 ├── api/
 ├── schemas/
 ├── controllers/
 ├── middleware/
 └── main.py

tests/
```

---

# Domain Layer

The domain layer represents the core concepts of the system.

It contains:

- **Value Objects** for strongly typed domain data.
- **Entities** with identity and lifecycle.
- **Domain Services** for logic that does not belong to a single entity.
- **Repository Interfaces** defining persistence contracts.
- **Domain Exceptions** for invariant violations.

This layer has no dependency on frameworks, databases, or external libraries.

---

## Value Objects

Value objects encapsulate validated domain data and prevent primitive‑obsession.

Examples include:

- `UserId`
- `ServiceName`
- `DomainName`
- `VaultItemUsername`
- `EncryptedValue`
- `CreatedAt`
- `UpdatedAt`
- and etc

Each value object ensures its own invariants and exposes the validated value.

---

## Entities

Entities represent domain objects with identity and lifecycle.

### User

Represents a registered user of the system.

Key characteristics:

- Identified by `UserId`
- Stores a hashed master password
- Verifies authentication through a domain service

Example behavior:

```
verify_master_password(password, hasher)
```

---

### Vault

Aggregate root representing a collection of stored credentials.

Responsibilities:

- Managing `VaultItem` entities
- Adding credentials
- Updating stored secrets
- Removing credentials
- Maintaining internal item ordering

Example behaviors:

```
add_item(...)
update_item_password(...)
remove_item(...)
```

---

### VaultItem

Represents a single stored credential.

A vault item is composed of value objects such as:

```
service_name
username
encrypted_password
domain_name
created_at
updated_at
```

Behavior includes updating credentials while maintaining timestamps.

---

## Domain Services

Domain services encapsulate logic that does not belong to a single entity.

Current services include:

- `MasterPasswordHasher`
- `PasswordStrengthCalculator`

Planned extensions include:

- `KeyDerivationService`
- `EncryptionService`

These services define interfaces within the domain while implementations live in the infrastructure layer.

---

## Repository Interfaces

Repositories define persistence contracts from the domain perspective.

Examples:

```
UserRepository
VaultRepository
```

These interfaces describe operations such as:

```
save(user)
get(user_id)
```

Infrastructure later provides concrete implementations.

---

# Application Layer

The application layer coordinates domain objects to implement use cases.

It contains no direct database access and no framework logic.

Typical responsibilities include:

- retrieving entities through repositories
- invoking domain behavior
- coordinating domain services
- returning structured responses

Examples of use cases:

- Register user
- Authenticate user
- Create vault
- Add vault item
- Update vault item
- Remove vault item

DTOs are used to isolate external representations from domain objects.

---

# Infrastructure Layer

The infrastructure layer implements technical concerns such as persistence and cryptography.

This layer includes:

- database configuration
- ORM models
- repository implementations
- cryptographic service implementations

Persistence is implemented using **PostgreSQL and SQLAlchemy**.

Security components include implementations of:

- password hashing
- encryption services
- key derivation mechanisms

Infrastructure depends on the domain but not vice versa.

---

# Interface Layer

The interface layer exposes Cryptora to external clients.

The primary interface is a **REST API built with FastAPI**.

Responsibilities include:

- defining HTTP routes
- validating requests
- invoking application use cases
- returning structured responses

The interface layer does not contain business logic.

---

# Testing

Tests are organized by architectural layer.

```
tests/
 ├── unit/domain
 ├── application
 ├── infrastructure
 └── api
```

Domain tests focus on:

- entity behavior
- value object invariants
- aggregate rules

This ensures that the core business logic remains correct independently of infrastructure or frameworks.

---

# Goals of the Project

Cryptora is designed with the following goals:

- clear separation of concerns
- explicit domain modeling
- cryptography isolated behind domain interfaces
- testable business logic
- infrastructure replaceability

The project is primarily focused on backend architecture and domain correctness rather than user interface concerns.

---

# Status

Cryptora is currently under active development.  
Core domain modeling and behavior are being implemented and tested.

Future work includes:

- completing application use cases
- implementing repository infrastructure
- integrating encryption services
- exposing API endpoints
- adding integration and and full e2e tests

---
Cryptora is an experimental project exploring secure system design, domain modeling, and maintainable backend architecture.
