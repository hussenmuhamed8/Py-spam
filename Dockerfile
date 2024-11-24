# استخدم صورة Python الأساسية
FROM python:3.9-slim

# تحديد دليل العمل داخل الحاوية
WORKDIR /app

# نسخ ملف المتطلبات إلى الحاوية
COPY requirements.txt requirements.txt

# تثبيت المكتبات المطلوبة
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات المشروع إلى الحاوية
COPY . .

# فتح المنفذ (اختياري إذا كان التطبيق يتطلب منفذًا مثل Flask)
EXPOSE 5000

# تشغيل ملف Python الرئيسي
CMD ["python", "Spam.py"]
