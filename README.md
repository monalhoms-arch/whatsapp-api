# 💬 WhatsApp Core Microservice

This directory contains the core microservice responsible for handling all communications, notifications, and database interactions for the **"Khidmati"** platform.

## 📌 Key Features
- **Security & OTP:** Manages the dissemination of highly secure OTP codes protected against spam using `Redis` rate-limiting.
- **Notifications Engine:** Handles direct and automated message dispatch to clients and workers.
- **Marketplace Management:** Controls the centralized PostgreSQL database (`whatsapp_data`) handling `provider` and `appointments` tables.
- **Evolution API Integration:** Formats and routes direct HTTP messages to the local Evolution API container network.

## 🛠️ Configuration
Ensure the `.env` file or constants are correctly set for:
- Evolution API endpoint (typically `http://localhost:8080`) and global API Token.
- `PostgreSQL` connection strings.
- `Redis` caching endpoint.

## 🚀 How to Run
Runs on **Port 8000**.
```bash
pip install -r requirements.txt
python main.py
```
> Swagger Interactive Docs available at: `http://localhost:8000/docs`
