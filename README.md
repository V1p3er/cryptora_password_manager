# 🔐 Password Manager (DDD Architecture)

A secure, modular, and scalable **Password Manager** built using **Domain-Driven Design (DDD)** principles.

This project is engineered to teach high-level backend design, security patterns, and clean architecture using Python.

---

## ⭐ Features

- Full DDD structure (Domain, Application, Infrastructure, Interfaces)
- AES-256 encryption using the `cryptography` library
- Argon2 key derivation for secure master passwords
- Encrypted vault stored locally (JSON or SQLite)
- Clean CLI built with `click`
- DTO-based application services
- Fully testable with unit, integration, and E2E tests
- Extensible (API support, desktop UI, browser extension)

---

## 📁 Project Structure

```
password_manager/
    domain/
    application/
    infrastructure/
    interfaces/
    tests/
```

Each layer is isolated:

- **Domain** — business rules, entities, value objects  
- **Application** — use cases  
- **Infrastructure** — encryption, storage, crypto, logs  
- **Interfaces** — CLI/API/UI  
- **Tests** — full test suite  

---

## 🚀 Getting Started

### 1) Create virtual environment

```
python -m venv venv
venv\Scripts\activate
```

### 2) Install dependencies

```
pip install -r requirements.txt
```

### 3) Run the CLI

```
python main.py
```

---

## 🔐 Security Notes

- Master password is never stored.
- Vault contents are encrypted using AES-256-GCM.
- Keys are derived with Argon2id.
- Side-channel protection included.
- Vault file integrity is verified on load.

Any compromise of the storage file does **not** reveal data.

---

## 🧪 Testing

Run the full test suite:

```
pytest -v
```


---

## 👤 Author

**Arman(v1p3er)**  
Entrepreneur • Programmer • Cybersecurity Enthusiast

---