from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import datetime
import json
import os
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

# Fayl nomi (Arxiv uchun - o'chib ketmaydi)
DB_FILE = "history.json"

# Seans tarixi - HAR SAFAR O'CHIRIB YOQQANDA BO'SH BO'LADI []
session_history = []

class Alert(BaseModel):
    status: str
    message: str

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
                .event-card { background: white; padding: 12px; margin-bottom: 10px; border-left: 5px solid #28a745; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
                h1 { color: #333; }
                .session-info { color: #d9534f; font-weight: bold; margin-bottom: 20px; }
                .time { color: #888; font-size: 12px; }
                .api-link { display: inline-block; margin-top: 20px; padding: 10px 15px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }
            </style>
            <script>
                function updateDashboard() {
                    // ?t=... qo'shish orqali brauzerni har safar yangi ma'lumot olishga majburlaymiz (keshni tozalaydi)
                    fetch('/api/status?t=' + new Date().getTime())
                    .then(response => response.json())
                    .then(data => {
                        let listHtml = "";
                        if(data.length === 0) {
                            listHtml = "<p>Hozircha ushbu seansda yangi xabarlar yo'q...</p>";
                        } else {
                            // Yangilari tepada chiqishi uchun reverse qilamiz
                            [...data].reverse().forEach(event => {
                                listHtml += `<div class="event-card">
                                                <span class="time">${event.time}</span><br>
                                                <strong>${event.message}</strong>
                                             </div>`;
                            });
                        }
                        document.getElementById('status-list').innerHTML = listHtml;
                    });
                }
                setInterval(updateDashboard, 1000);
            </script>
        </head>
        <body>
            <h1>Live Session Monitoring</h1>
            <p class="session-info">DIQQAT: Server qayta yoqildi. Faqat yangi ma'lumotlar ko'rsatiladi.</p>
            <a href="/docs" class="api-link" target="_blank">API Hujjatlari (Swagger UI)</a>
            <div id="status-list" style="margin-top: 20px;">Yuklanmoqda...</div>
        </body>
        </html>
    """

@app.post("/api/alert")
async def receive_alert(alert: Alert):
    global session_history
    
    new_event = {
        "status": alert.status,
        "message": alert.message,
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # 1. Seansga qo'shish
    session_history.append(new_event)

    # 2. Arxivga (history.json) qo'shish
    archive_to_json(new_event)

    return {"res": "ok"}

@app.get("/api/status")
async def get_status():
    return session_history

if __name__ == "__main__":
    # Server yonganini terminalda ko'rish uchun
    print("\n" + "=" * 30)
    print("YANGI SEANS BOSHLANDI!")
    print("API docs: http://localhost:5000/docs")
    print("=" * 30 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=5000)