# 🔐 Cryptora

Cryptora is an advanced, enterprise‑grade open‑source **Password Manager** built on a clean, modular backend architecture with a strong focus on security, scalability, and long‑term maintainability.

The project follows **Clean Architect** and modern software engineering principles to provide a solid foundation for production‑level credential storage systems.

---

## ⭐ Key Features

- Structured DDD layout (Domain, Application, Infrastructure, Interfaces)
- AES‑256‑GCM encryption powered by the `cryptography` library
- Argon2id key derivation for strong master password security
- Fully encrypted vault stored locally (JSON or SQLite backend)
- CLI interface built with `click`
- DTO‑driven application services and clean use‑case separation
- Comprehensive test coverage (unit, integration, E2E)
- Designed for extension (REST API, desktop client, browser extension, mobile)

---

## 📁 Project Structure

```
cryptora/
    domain/
    application/
    infrastructure/
    interfaces/
    tests/
```

**Layer overview:**

- **Domain** — entities, aggregates, value objects, core business logic  
- **Application** — use cases and service orchestration  
- **Infrastructure** — crypto utilities, storage adapters, logging  
- **Interfaces** — CLI, future API/UI layers  
- **Tests** — full automated test suite  

---

## 🚀 Getting Started

### 1) Create and activate a virtual environment

```
python -m venv venv
venv\Scripts\activate
```

### 2) Install dependencies

```
pip install -r requirements.txt
```

### 3) Launch the CLI

```
python main.py
```

---

## 🔐 Security Overview

- Master password is never stored or cached.
- All vault data is encrypted using AES‑256‑GCM.
- Key stretching and derivation handled by Argon2id.
- Storage file includes integrity verification.
- No plaintext secrets written to disk at any point.

A compromised vault file alone does **not** disclose any user data.

---

## 🧪 Testing

Run all tests:

```
pytest -v
```

---

## 👤 Author

**Arman (v1p3er)**  
Entrepreneur • Backend Developer • Cybersecurity Enthusiast