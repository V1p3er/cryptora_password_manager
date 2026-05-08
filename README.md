# 🔐 Cryptora — Password Manager Engine

**A security‑first, extensible password manager engine built with Clean Architecture and industry‑grade cryptography.**  
Designed and engineered by **Arman (v1p3er)**

---

## 🧠 Philosophy: Why Cryptora Exists

> *"Most password managers are secure. Very few are well‑designed."*

Cryptora began as a response to that paradox.  
It is not another feature‑stacked app — it’s an **architectural foundation** for building password management systems that are easy to reason about, secure by design, and open for developers to customize.

Where most tools blur the boundary between logic, encryption, and storage, **Cryptora separates concerns at the structural level**:
- Cryptography belongs to *domain services*, not models.
- Validation and invariants live in *Value Objects*, not helpers.
- Storage is *replaceable* (PostgreSQL, JSON, etc.).
- The system is **configurable** — from a CLI tool to a full server+UI environment.

---

## 🏗️ Architecture Overview

Cryptora follows the **Clean Architecture** pattern — every dependency points inward to the Domain.

```
┌────────────────────────────┐
│         Interfaces         │   ← CLI, API, Desktop app, Extensions
└──────────────▲─────────────┘
               │
┌──────────────┴─────────────┐
│        Application         │   ← Use‑cases, DTOs, Services
└──────────────▲─────────────┘
               │
┌──────────────┴─────────────┐
│          Domain            │   ← Entities, Value Objects, Domain Services
└──────────────▲─────────────┘
               │
┌──────────────┴─────────────┐
│       Infrastructure       │   ← Crypto, Persistence, Config, Security
└────────────────────────────┘
```

### Key Concepts
- **Domain Core is pure Python:** No imports from frameworks or external libraries.  
- **Infrastructure is plug‑replaceable:** Swap cryptography provider, storage engine, or random key derivation without touching domain code.  
- **Interfaces are modular:** CLI, REST API, or local app — all can plug into the same Application layer.

---

## 📦 Current Modules

### **Domain Layer**
Contains the business rules and secure data representations:
- `entities/` → `User`, `Vault`, `Credential`
- `value_objects/` → immutable value types such as:
  - `UserId`, `Username`, `MasterPassword`, `PasswordHash`
  - `EncryptedValue`, `PasswordStrength`
  - `CreatedAt`, `UpdatedAt`, `ServiceName`, `DomainName`
- `services/` → crypto‑related domain behaviors:
  - `EncryptionService`
  - `KeyDerivationService`
  - `VaultPolicyService`
- `repositories/` → abstract interfaces (`VaultRepository`)

---

### **Application Layer**
Implements use cases and orchestrates logic between domain and interfaces:
- `services/`  
  - `create_vault.py`, `unlock_vault.py`, `add_credential.py`, etc.  
  - each service enforces security policies and transactional flow.
- `dto/`  
  - `credential_dto.py`, `vault_dto.py`
- `exceptions/`  
  - typed domain errors (e.g. `InvalidMasterPasswordError`)

---

### **Infrastructure Layer**
Handles system‑level concerns with pluggable implementations:
- **config/**
  - `settings.py` — environment‑aware configuration
- **crypto/**
  - `argon2_key_derivation.py` — Argon2id hashing  
  - `cryptography_encryption.py` — Fernet / AES encryption  
  - `secure_random.py` — strong non‑predictable RNG
- **persistence/**
  - `postgresql_vault_repository.py` — PostgreSQL backend  
  - `file_vault_repository.py` — JSON‑based local store
- **security/**
  - `audit_logger.py`, `integrity_checker.py`, `password_hasher.py`

Each component can be registered dynamically at startup via a config file, allowing **users or developers** to choose:
- local storage (JSON)
- server‑based PostgreSQL
- or hybrid configuration (e.g. local caching, remote sync)

---

### **Interfaces Layer**
This is how Cryptora talks to the outside world.
- **CLI** → `vault_cli.py`, `menu.py`  
  (for local use, no internet required)
- **API** → `routes.py`, `request_models.py`, `response_models.py`
- **Desktop (future)** → `app.py`
- **Extensions** → cryptora modules can be imported into other apps as a secure vault backend  

The system is **backend‑agnostic**, meaning your UI, extension, or automation script can interact with Cryptora the same way — through its **Application Services**.

---

## 🧩 Extensibility Vision

Cryptora isn’t just a password manager.  
It’s an **encryption and credential management engine** that others can build on top of.

### Usage Scenarios
- 🖥 **Local user vault** → stored as `.json` file (offline mode)  
- ☁️ **Server deployment** → PostgreSQL + API layer for multi‑device sync  
- 🔌 **Integration mode** → expose REST or gRPC endpoints for developers  
- 🧩 **Extension mode** → UI plugins (browser, desktop) built on the same backend

With future `cryptora.config` APIs, users can define how they want the vault to behave:
```python
CRYPTO_BACKEND = "cryptography_encryption.Fernet"
STORAGE_BACKEND = "postgresql_vault_repository.PostgreSQLVaultRepository"
AUDIT_LOGS = True
```

---

## 🔐 Security Model

- All sensitive data encrypted using **Fernet (AES‑128 in CBC mode with HMAC‑SHA256)**
- Master password hashed via **Argon2id**
- Key derivation isolated from storage
- All value objects immutable and validated
- Audit logging and integrity checking built into infrastructure
- Security measures inspired by OWASP, Signal’s cryptographic patterns, and domain‑driven constraints

---

## 🧪 Testing Structure

```
tests/
  ├── unit/
  │   └── domain/value_objects/
  │       ├── test_encrypted_value.py
  │       ├── test_password_hash.py
  │       └── …
  ├── integration/
  └── e2e/
      └── full_test.py
```

Focus:
- Behavior verification of each VO and service  
- Security invariants enforced (invalid keys, malformed ciphertext, etc.)  
- End‑to‑end vault encryption lifecycle  
- No cryptographic primitives are mocked in unit tests

---

## ⚙️ Configuration Philosophy

Cryptora is built for **both everyday users and developers**.  
You can run it as:
- 💻 A self‑contained local vault (JSON files)
- 🖲️ A CLI password manager
- 🌐 A server‑based system using PostgreSQL
- 🧩 A security engine embedded into other apps

Configuration lives under `config/settings.py`  
– everything from cryptographic parameters to data repository selection is adjustable.

---

## 🤝 Contributing

Contributions are welcome — especially those focusing on:
- Security audits
- New persistence adapters
- Developer documentation
- CLI / API improvements

Before submitting a pull request:
1. Run all tests with `pytest`
2. Follow PEP‑8 & Clean Architecture guidelines
3. Sign commits with your GPG key  
4. Read [`CONTRIBUTING.md`](./CONTRIBUTING.md)

---

## 📜 License

Licensed under the **Apache License 2.0**

```
Copyright 2026 Arman (v1p3er)
Originator of the Cryptora™ password management engine.
```

---

## 🏴 Author Verification

🔏 **All commits are GPG‑signed and verified** on GitHub.

| Field | Info |
|-------|------|
| Project | Cryptora |
| Author | Arman (v1p3er) |
| Founded | May 2026 |
| Verification | GPG Key ID B1369B968C9BDFA2 |

---

## 🧭 Vision

> **Cryptora is not “another password manager.”**  
> It’s a *secure foundation* for how encryption, storage, and architecture should interact — minimal, composable, and verifiable.

Cryptora’s ultimate goal is to become a **developer‑friendly security framework** that anyone can embed or extend:
- Security researchers can audit the cryptographic design transparently.  
- Developers can plug it into their own tools as a vault engine.  
- End users can run it offline with zero trust in remote services.  
- Organizations can deploy it on their infrastructure with their own compliance standards.

Every part of Cryptora – from the **Argon2id hashing layer** to the **domain model purity** – is built with one philosophy:

> **“Security by architecture, not by accident.”**
