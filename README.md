# WhatsApp Microservice API

A standalone, production-ready WhatsApp microservice built with **FastAPI**, **Redis**, and **PostgreSQL**.
This service acts as an abstraction layer to connect any SaaS (like Labor Rental Systems) to WhatsApp APIs (e.g., Evolution API, Baileys, Meta API).

## 🚀 Features
- **API Security**: All endpoints protected via `X-API-KEY`.
- **Advanced OTP System**: 
  - Generates secure random codes.
  - Codes are **hashed via bcrypt** before caching.
  - Automatically expires codes via **Redis TTL (5 Mins)**.
  - **Smart Rate-Limiting**: Blocks users for 15 minutes after 3 failed attempts.
- **Asynchronous Execution**: Uses FastAPI `BackgroundTasks` to queue messages instantly (Returns 200 OK without blocking), ensuring the main SaaS doesn't face latency issues.
- **Dockerized**: Fully deployable via `docker-compose`.

## 🛠️ Stack
- **FastAPI** (Python 3.10+)
- **Redis** (OTP & Blocks)
- **PostgreSQL** (Accounts Database)
- **Evolution API** (WhatsApp Gateway)

## 🐳 Easy Deployment (Docker)
1. Clone the repository:
   ```bash
   git clone https://github.com/monalhoms-arch/whatsapp-api.git
   cd whatsapp-api
   ```
2. Configure your Environment Variables:
   - Create a `.env` file referencing the structure of `config.py`.
3. Launch with Docker Compose:
   ```bash
   docker-compose up -d --build
   ```
This will spin up the API (`8000`), a PostgreSQL DB, and a Redis Cache.

## 🔐 Endpoints Structure
- `/api/v1/otp/send`: Generates OTP and dispatches WhatsApp background request.
- `/api/v1/otp/verify`: Strict OTP verification using Redis Hash matches.
- `/api/v1/notifications/send`: Sends dynamic messages based on user constraints (Customer, Provider, Admin).

## 📝 Logging
Powered by **Loguru** to maintain detailed audit logs for every request attempt, block action, or message dispatch failure.
