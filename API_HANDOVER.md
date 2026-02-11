# API Dokumentatsiyasi (Jamoangiz uchun)

Salom! Bizning AI Detektor tizimimiz uchun API tayyor. Quyidagi ma'lumotlarni ishlatishingiz mumkin.

## 🔗 Asosiy URL (Base URL)
Barcha so'rovlar shu manzilga yuboriladi:
> **`https://ai-detector-e2x2.onrender.com`**

## 📚 To'liq Hujjatlar (Swagger UI)
API qanday ishlashini ko'rish va test qilish uchun:
> **[https://ai-detector-e2x2.onrender.com/docs](https://ai-detector-e2x2.onrender.com/docs)**

---

## ⚡️ API Endpoints

### 1. Xavf haqida xabar berish (POST)
Detektor yoki boshqa qurilma xavfni aniqlasa, shu yerga so'rov yuboradi.

**DIQQAT:** Bu endpoint endi **`multipart/form-data`** qabul qiladi (Rasm yuborish uchun).

**URL:** `/api/alert`
**Method:** `POST`
**Body (Form Data):**
*   `status`: "danger" (Matn)
*   `message`: "DIQQAT: ..." (Matn)
*   `file`: (Fayl/Rasm - Opsional)

### 2. Holatni olish (GET)
So'nggi hodisalar tarixini olish uchun.

**URL:** `/api/status`
**Method:** `GET`
**Javob (Response):**
```json
[
  {
    "status": "danger",
    "message": "DIQQAT: ...",
    "time": "2024-02-10 15:30:00",
    "image_url": "/static/images/alert_170756.jpg" (agar rasm bo'lsa)
  },
  ...
]
```
