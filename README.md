# AI Xavfsizlik Tizimi (AI Detector)

Bu loyiha videokuzatuv orqali taqiqlangan hududga o'tishni aniqlash va serverga xabar yuborish tizimi.

## 📁 Fayllar Tushuntirishi
*   **server.py**: Internetga (Renderga) yuklanadigan asosiy fayl.
*   **detector.py**: Sizning kompyuteringizda ishlaydigan va kameradan kuzatadigan dastur.
*   **requirements.txt**: Server uchun kerakli kutubxonalar (Yengil).
*   **requirements_detector.txt**: Detektor uchun kerakli kutubxonalar (Og'ir).

---

## 🚀 Serverni Renderga Yuklash (Deploy)

1.  Ushbu loyihani **GitHub** ga yuklang.
2.  [Render.com](https://render.com) saytiga kiring va ro'yxatdan o'ting.
3.  "New" -> "Web Service" ni tanlang.
4.  GitHub repozitoriyni tanlang.
5.  Quyidagi sozlamalarni kiriting:
    *   **Name:** `ai-detector` (yoki xohlagan nom)
    *   **Runtime:** `Python 3`
    *   **Build Command:** `pip install -r requirements.txt`
    *   **Start Command:** `uvicorn server:app --host 0.0.0.0 --port $PORT`
6.  "Create Web Service" tugmasini bosing.

Server ishga tushgach, sizga **URL** beriladi (masalan: `https://ai-detector.onrender.com`).

---

## 📷 Detektorni Sozlash (Kompyuterda)

Server internetga chiqib bo'lgach:

1.  **Kutubxonalarni o'rnatish** (Agar hali o'rnatilmagan bo'lsa):
    ```bash
    pip install -r requirements_detector.txt
    ```

2.  **Manzilni o'zgartirish**:
    `detector.py` faylani ochib, `SERVER_URL` ni yangilang:
    ```python
    # Renderdagi manzil:
    SERVER_URL = "https://ai-detector.onrender.com/api/alert"
    ```

3.  **Ishga tushirish**:
    ```bash
    python detector.py
    ```

## 📄 API
API hujjatlarini ko'rish uchun server manzilingiz oxiriga `/docs` qo'shing:
`https://ai-detector.onrender.com/docs`
