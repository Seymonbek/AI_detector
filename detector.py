import cv2
from ultralytics import YOLO
import requests

# 1. Modelni yuklash
model = YOLO('yolov8n.pt')

# 2. Videoni yuklash
cap = cv2.VideoCapture("test_video.mp4")

# AGAR SERVERGA YUKLASANGIZ, BU YERGA SERVER IP MANZILINI YOZING!
# Masalan: "http://192.168.1.100:5000/api/alert" yoki "https://mening-saytim.com/api/alert"
SERVER_URL = "http://127.0.0.1:5000/api/alert"

# Odamlarning oldingi kordinatalarini saqlash uchun (oddiyroq usul)
# Kalit sifatida odamning tartib raqami yoki koordinatasi ishlatiladi
prev_positions = {}

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    height, width, _ = frame.shape
    LINE_X = width // 2

    # persist=True trackingni yoqadi
    results = model.track(frame, persist=True, verbose=False, conf=0.5)

    danger_now = False

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
                    danger_now = True
                    print(f"DIQQAT: ID {obj_id} o'ngdan chapga o'tdi!")

            # Pozitsiyani yangilash
            prev_positions[obj_id] = current_x

            # Vizualizatsiya
            color = (0, 0, 255) if current_x < LINE_X else (0, 255, 0)
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            cv2.putText(frame, f"ID:{obj_id}", (int(x1), int(y1)-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Serverga faqat xavf bo'lganda yuborish
    if danger_now:
        try:
            requests.post(SERVER_URL, json={
                "status": "danger",
                "message": "DIQQAT: Odam taqiqlangan yo'nalishda (o'ngdan chapga) o'tdi!"
            }, timeout=0.1)
        except: pass

    # Chiziqni chizish
    cv2.line(frame, (LINE_X, 0), (LINE_X, height), (255, 255, 0), 2)
    cv2.imshow("Direction Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()