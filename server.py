from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import datetime
import json
import os
import shutil
import uvicorn

app = FastAPI(
    title="AI Detection API",
    description="API for AI Detector System with Dashboard",
    version="1.0.0"
)

# CORS sozlamalari
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rasmlarni saqlash uchun papka
os.makedirs("static/images", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Fayl nomi (Arxiv uchun - o'chib ketmaydi)
DB_FILE = "history.json"

# Seans tarixi - HAR SAFAR O'CHIRIB YOQQANDA BO'SH BO'LADI []
session_history = []

def archive_to_json(new_event):
    data = []
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            data = []
    
    # Ro'yxat boshiga emas, oxiriga qo'shamiz
    data.append(new_event)
    
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>AI Monitoring - Pure Session</title>
            <style>
                body { font-family: sans-serif; background: #f4f4f4; padding: 20px; }
                .event-card { background: white; padding: 15px; margin-bottom: 15px; border-left: 5px solid #28a745; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
                .event-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
                .time { color: #888; font-size: 14px; }
                .message { font-size: 16px; font-weight: bold; color: #333; }
                .event-image { max-width: 100%; border-radius: 5px; margin-top: 10px; border: 1px solid #ddd; }
                h1 { color: #333; text-align: center; }
                .session-info { text-align: center; color: #d9534f; font-weight: bold; margin-bottom: 20px; }
                .api-link { display: block; text-align: center; margin-top: 20px; color: #007bff; text-decoration: none; }
                #status-list { max-width: 600px; margin: 0 auto; }
            </style>
            <script>
                function updateDashboard() {
                    // ?t=... qo'shish orqali brauzerni har safar yangi ma'lumot olishga majburlaymiz (keshni tozalaydi)
                    fetch('/api/status?t=' + new Date().getTime())
                    .then(response => response.json())
                    .then(data => {
                        let listHtml = "";
                        if(data.length === 0) {
                            listHtml = "<p style='text-align:center'>Hozircha ushbu seansda yangi xabarlar yo'q...</p>";
                        } else {
                            // Yangilari tepada chiqishi uchun reverse qilamiz
                            [...data].reverse().forEach(event => {
                                let imageHtml = "";
                                if (event.image_url) {
                                    imageHtml = `<img src="${event.image_url}" class="event-image" alt="Detection Image">`;
                                }
                                
                                listHtml += `<div class="event-card">
                                                <div class="event-header">
                                                    <span class="time">${event.time}</span>
                                                </div>
                                                <div class="message">${event.message}</div>
                                                ${imageHtml}
                                             </div>`;
                            });
                        }
                        document.getElementById('status-list').innerHTML = listHtml;
                    });
                }
                setInterval(updateDashboard, 2000); // Har 2 soniyada yangilash
            </script>
        </head>
        <body>
            <h1>Live AI Monitoring</h1>
            <p class="session-info">DIQQAT: Server qayta yoqildi. Faqat yangi ma'lumotlar ko'rsatiladi.</p>
            <div id="status-list">Yuklanmoqda...</div>
            <a href="/docs" class="api-link" target="_blank">API Hujjatlari (Swagger UI)</a>
        </body>
        </html>
    """

@app.post("/api/alert")
async def receive_alert(
    status: str = Form(...), 
    message: str = Form(...),
    file: UploadFile = File(None)
):
    global session_history
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    image_url = None

    # Agar rasm yuborilgan bo'lsa, saqlaymiz
    if file:
        file_ext = file.filename.split(".")[-1]
        filename = f"alert_{int(datetime.datetime.now().timestamp())}.{file_ext}"
        file_path = f"static/images/{filename}"
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # URL (Masalan: /static/images/alert_123456.jpg)
        image_url = f"/static/images/{filename}"

    new_event = {
        "status": status,
        "message": message,
        "time": timestamp,
        "image_url": image_url
    }

    # 1. Seansga qo'shish
    session_history.append(new_event)

    # 2. Arxivga (history.json) qo'shish
    archive_to_json(new_event)

    return {"res": "ok", "image_url": image_url}

@app.get("/api/status")
async def get_status():
    return session_history

if __name__ == "__main__":
    # Server yonganini terminalda ko'rish uchun
    print("\n" + "=" * 30)
    print("YANGI SEANS BOSHLANDI (RASMLAR BILAN)!")
    print("API docs: http://localhost:5000/docs")
    print("=" * 30 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=5000)