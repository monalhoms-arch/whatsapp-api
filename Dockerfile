FROM python:3.10-slim

# تعيين المجلد الأساسي للتطبيق داخل الحاوية
WORKDIR /app

# منع بايثون من كتابة ملفات .pyc وإرسال السجلات للـ stdout مباشرة
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# تثبيت المنظومات الأساسية للنظام (لأجل psycopg2 وغيره)
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# نسخ وتثبيت الحزم
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات المشروع
COPY . .

# فتح بورت 8000
EXPOSE 8000

# أمر تشغيل السيرفر
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
