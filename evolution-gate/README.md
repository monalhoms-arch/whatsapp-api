# 🚀 Evolution Manager & WhatsApp Gateway Setup Guide (Evolution API v2)

## English / العربية

**This folder contains everything to run real WhatsApp gateway & auto-send messages from "خدمتي" system.**

هذا المجلد يحتوي على كل ما تحتاجه لتشغيل بوابة واتساب حقيقية وإرسال الرسائل آلياً من نظام "خدمتي".

## 🛠️ خطوات التشغيل

### 1. Start Services (Docker) / تشغيل الخدمات

**English:** Install Docker Desktop (https://www.docker.com/products/docker-desktop/), start it, then run:
```bash
cd evolution-gate
docker compose up -d
```

**Check status:** `docker compose ps` or `docker compose logs evolution_api`

**العربية:** تأكد من تثبيت **Docker Desktop** وتشغيله، ثم:
```bash
cd evolution-gate
docker compose up -d
```
تحقق: `docker compose ps` أو `docker compose logs evolution_api`

### 2. Login to Evolution Manager / تسجيل الدخول

**English:**  
1. Open http://localhost:3000  
2. The Manager will auto-connect to Evolution API assuming `http://evolution_api:8080` (or `http://localhost:8080`)  
3. Use the global API Key: `my_evolution_token_123`  

**العربية:**  
1. افتح http://localhost:3000  
2. مدير البوابة سيتصل بـ Evolution API تلقائياً.  
3. استخدم الـ API Key: `my_evolution_token_123`  

### 3. Access Manager Dashboard / مدير البوابة
**English:** After login, you are in the Manager.

**العربية:** بعد الدخول, ستكون داخل مدير البوابة.

### 4. Create Instance & Pair Phone / إنشاء Instance وربط الهاتف

**English:**  
1. In Manager (http://localhost:8080/manager), create new instance named `main_instance`.  
2. Scan QR code with WhatsApp (Linked Devices > Link Device).  
3. Status: Connected.

**العربية:**  
1. في المدير (http://localhost:8080/manager), أنشئ instance باسم `main_instance`.  
2. امسح QR من WhatsApp (الأجهزة المرتبطة > ربط جهاز).  
3. الحالة: متصل.

## 🔗 الربط مع مشروعك

**API Key source:** evolution-gate/docker-compose.yml (AUTHENTICATION_API_KEY=my_evolution_token_123)

**Integration:** Matches whatsapp/config.py EVOLUTION_API_URL & INSTANCE_NAME=main_instance. Update token if changed.

**العربية:** المفتاح من docker-compose.yml. يطابق إعدادات whatsapp/config.py.

### 5. Project Integration / الربط مع المشروع

**English:** Edit whatsapp/config.py or .env:  
`EVOLUTION_INSTANCE_NAME=main_instance`

**API Key:** `my_evolution_token_123` (docker-compose.yml)

### 6. Final Test / الاختبار النهائي

**English:** Dashboard > WhatsApp/Marketplace tab > Enable auto-send > Test worker.

**العربية:** لوحة التحكم > Marketplace > فعل "الإرسال الآلي" > اختبر عامل.
الرسالة تصل آلياً!

---
> [!TIP]  
> **Demo tip:** Ensure Docker running & phone online for live QR scan demo.  
> **العربية:** في يوم المناقشة، تأكد من أن Docker يعمل وهاتفك متصل لتجربة مبهرة.

### 7. Troubleshooting & Stop / استكشاف الأخطاء

**English:**  
- Services not starting? `docker compose logs evolution_api`  
- No login? Check API key.  
- Stop: `docker compose down -v` (remove data) or `docker compose down`.

**العربية:**  
- مشاكل؟ `docker compose logs evolution_api`  
- Stop: `docker compose down`.

> [!NOTE]  
> Volumes persist DB data.
