import cv2
from ultralytics import YOLO
import requests
import time
import threading

# 1. Modelni yuklash
model = YOLO('yolov8n.pt')

# 2. Videoni yuklash
cap = cv2.VideoCapture("test_video.mp4")

# AGAR SERVERGA YUKLASANGIZ, BU YERGA SERVER IP MANZILINI YOZING!
SERVER_URL = "https://ai-detector-e2x2.onrender.com/api/alert"

# Dastur boshlanishida server tarixini tozalash (Reset)
try:
    print("Server tarixi tozalanmoqda...")
    requests.post(SERVER_URL.replace("/alert", "/reset"), timeout=5)
    print("✅ Server tozalandi!")
except Exception as e:
    print(f"⚠️ Serverni tozalashda xatolik: {e}")

# Xabar yuborish chastotasini cheklash (Cooldown)
# Har bir ID uchun alohida vaqt saqlaymiz: {obj_id: timestamp}
last_alert_times = {}

# Odamlarning oldingi kordinatalarini saqlash uchun (oddiyroq usul)
# Kalit sifatida odamning tartib raqami yoki koordinatasi ishlatiladi
prev_positions = {}

def send_alert_thread(url, data, files, obj_id):
    try:
        response = requests.post(url, data=data, files=files, timeout=30)
        if response.status_code == 200:
            print(f"✅ ID {obj_id} yuborildi! Javob: {response.text}")
        else:
            print(f"❌ ID {obj_id} xatolik: {response.status_code}")
    except Exception as e:
        print(f"❌ ID {obj_id} ulanish xatosi: {e}")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    height, width, _ = frame.shape
    LINE_X = width // 2

    # Chiziqni chizish (Avval chizamiz, shunda rasmda ko'rinadi)
    cv2.line(frame, (LINE_X, 0), (LINE_X, height), (255, 255, 0), 2)

    # persist=True trackingni yoqadi
    results = model.track(frame, persist=True, verbose=False, conf=0.5)

    # Agar kadrda ob'ektlar aniqlangan bo'lsa
    if results[0].boxes is not None and results[0].boxes.id is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy()
        ids = results[0].boxes.id.int().cpu().tolist()

        for box, obj_id in zip(boxes, ids):
            x1, y1, x2, y2 = box
            current_x = (x1 + x2) / 2 # Odamning markazi

            # Agar bu ID oldin ko'ringan bo'lsa
            if obj_id in prev_positions:
                old_x = prev_positions[obj_id]

                # YO'NALISH: O'NGDAN -> CHAPGA (LINE_X dan o'tish)
                if old_x >= LINE_X and current_x < LINE_X:
                    print(f"DIQQAT: ID {obj_id} o'ngdan chapga o'tdi!")
                    
                    # FAQAT shu odamni chizamiz (xavf bo'lganda)
                    color = (0, 0, 255) # Qizil
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                    cv2.putText(frame, f"ID:{obj_id}", (int(x1), int(y1)-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    
                    # Cooldown tekshirish (Shu ID uchun)
                    current_time = time.time()
                    last_time = last_alert_times.get(obj_id, 0)
                    
                    if current_time - last_time > 120:
                        print(f"XAVF ANIQLANDI! Fon rejimida yuborilmoqda...")
                        
                        # Rasmni tayyorlash (siqish)
                        _, img_encoded = cv2.imencode('.jpg', frame)
                        img_bytes = img_encoded.tobytes()
                        
                        # Ma'lumotlar
                        files = {'file': ('alert.jpg', img_bytes, 'image/jpeg')}
                        data = {
                            "status": "danger",
                            "message": f"DIQQAT: Ob'ekt {obj_id} taqiqlangan yo'nalishda (o'ngdan chapga) o'tdi!"
                        }
                        
                        # Alohida oqimda (Thread) yuborish - Dastur qotib qolmaydi
                        threading.Thread(target=send_alert_thread, args=(SERVER_URL, data, files, obj_id)).start()
                        
                        last_alert_times[obj_id] = current_time # Vaqtni yangilaymiz
                    else:
                        print(f"⚠️ ID {obj_id} uchun cooldown (kutish) rejimi.")

            # Pozitsiyani yangilash
            prev_positions[obj_id] = current_x

    cv2.imshow("Direction Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()