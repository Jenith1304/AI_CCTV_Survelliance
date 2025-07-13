# import cv2
# import os
# import csv
# import subprocess
# from datetime import datetime
# from ultralytics import YOLO
# import numpy as np
# from bson import ObjectId
# from app.extensions import mongo
# from app.utils.email_utils import send_alert_email

# # --- Paths ---
# MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model-training", "runs", "detect", "train2", "weights", "best.pt"))
# FFMPEG_PATH = r"C:\\ffmpeg-master-latest-win64-gpl-shared\\bin\\ffmpeg.exe"
# STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
# LOG_PATH = os.path.join("logs", "zone_log.csv")

# # --- Initialization ---
# model = YOLO(MODEL_PATH)
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# helmet_last_alert_time = None
# helmet_cooldown_seconds = 60
# last_alert_time = {}
# zone_status = {}  # Make sure zone status is tracked globally

# # --- Create log directory ---
# os.makedirs("logs", exist_ok=True)
# if not os.path.exists(LOG_PATH):
#     with open(LOG_PATH, 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(["Time", "Zone", "Face_ID", "Helmet", "Event"])

# # --- Utility ---
# def get_zones_for_user(user_id):
#     # print("User")
#     # print(user_id)
#     zones_cursor = mongo.db.zones.find({"user_id": ObjectId(user_id)})
#     # print(zones_cursor)
#     return {
#         zone['zone_name']: {
#             'x1': int(zone['x1']),
#             'y1': int(zone['y1']),
#             'x2': int(zone['x2']),
#             'y2': int(zone['y2'])
#         }
#         for zone in zones_cursor
#     }

# def get_iou(boxA, boxB):
#     xA, yA = max(boxA[0], boxB[0]), max(boxA[1], boxB[1])
#     xB, yB = min(boxA[2], boxB[2]), min(boxA[3], boxB[3])
#     interArea = max(0, xB - xA) * max(0, yB - yA)
#     boxAArea = (boxA[2]-boxA[0]) * (boxA[3]-boxA[1])
#     boxBArea = (boxB[2]-boxB[0]) * (boxB[3]-boxB[1])
#     return interArea / float(boxAArea + boxBArea - interArea + 1e-6)

# def point_in_zone(x, y, zone):
#     return zone['x1'] <= x <= zone['x2'] and zone['y1'] <= y <= zone['y2']

# def log_event(user_id, zone_name, face_id, helmet_status, event_type):
#     try:
#         print(f"[LOGGED] {event_type} | {zone_name} | {face_id} | {helmet_status}")
#         mongo.db.detections.insert_one({
#             "user_id": user_id,
#             "zone": zone_name,
#             "face_id": face_id,
#             "helmet": helmet_status,
#             "event": event_type,
#             "timestamp": datetime.utcnow()
#         })
#     except Exception as e:
#         print(f"[ERROR] Failed to log detection: {e}")

# # --- Process Frame ---
# def process_frame(frame, user=None):
#     global helmet_last_alert_time, zone_status

#     user_id = user
   
#     if not user_id:
#         print("[ERROR] user_id is None")
#         return frame

#     zones = get_zones_for_user(user_id)
#     if not zones:
#         print("[WARN] No zones found for user.")
#         return frame

#     timestamp = datetime.now()
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, 1.2, 5)

#     results = model(frame)[0]
#     helmet_boxes = [tuple(map(int, box.xyxy[0])) for box in results.boxes if results.names[int(box.cls[0])] == "helmet"]

#     zone_occupied = {z: False for z in zones}
#     helmet_violation = False
#     unattended_zones = []

#     for i, (x, y, w, h) in enumerate(faces):
#         center_x, center_y = x + w // 2, y + h // 2
#         face_id = f"Face_{i}"

#         cv2.circle(frame, (center_x, center_y), 5, (255, 255, 255), -1)
#         cv2.putText(frame, "Center", (center_x + 5, center_y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

#         helmet_found = any(get_iou((x, y, x + w, y + h), hb) > 0.2 for hb in helmet_boxes)
#         helmet_status = "Helmet" if helmet_found else "No Helmet"
#         color = (0, 255, 0) if helmet_found else (0, 0, 255)

#         cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
#         cv2.putText(frame, f"{face_id} - {helmet_status}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

#         if not helmet_found:
#             helmet_violation = True

#         in_any_zone = False

#         for zone_name, zone in zones.items():
#             in_zone = point_in_zone(center_x, center_y, zone)
#             key = (face_id, zone_name)

#             if in_zone:
#                 in_any_zone = True
#                 zone_occupied[zone_name] = True
#                 if not zone_status.get(key):
#                     log_event(user_id, zone_name, face_id, helmet_status, "Entered")
#                     zone_status[key] = True
#             elif zone_status.get(key):
#                 log_event(user_id, zone_name, face_id, helmet_status, "Exited")
#                 zone_status[key] = False

#         if not in_any_zone:
#             print(f"[SKIP] {face_id} not in any zone. No logging.")

#     for zone_name, occupied in zone_occupied.items():
#         if not occupied:
#             last_time = last_alert_time.get(zone_name)
#             if not last_time or (timestamp - last_time).total_seconds() > 60:
#             # ⚠️ Log unattended event
#                 log_event(
#                 user_id=user_id,
#                 zone_name=zone_name,
#                 face_id="None",
#                 helmet_status="None",
#                 event_type="Unattended"
#                 )
#                 last_alert_time[zone_name] = timestamp
#                 z = zones[zone_name]
#                 cv2.rectangle(frame, (z["x1"], z["y1"]), (z["x2"], z["y2"]), (0, 0, 255), 2)

#     if helmet_violation and (not helmet_last_alert_time or (timestamp - helmet_last_alert_time).total_seconds() > helmet_cooldown_seconds):
#         send_alert_email(user=user_id, detections=["No Helmet"], zones=unattended_zones)
#         helmet_last_alert_time = timestamp
#     elif unattended_zones:
#         send_alert_email(user=user_id, detections=[], zones=unattended_zones)

#     for zone_name, coords in zones.items():
#         cv2.rectangle(frame, (coords["x1"], coords["y1"]), (coords["x2"], coords["y2"]), (255, 255, 0), 2)
#         cv2.putText(frame, zone_name, (coords["x1"], coords["y1"] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

#     return frame

# # --- Image ---
# def detect_image(image_path, user=None):
#     frame = cv2.imread(image_path)
#     processed = process_frame(frame, user=user)
#     output_path = os.path.join(STATIC_DIR, "output.jpg")
#     cv2.imwrite(output_path, processed)
#     return output_path

# # --- Video ---
# def detect_video(video_path, user=None, output_folder="custom_video_output"):
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     video_abs_path = os.path.abspath(video_path)

#     results = model.predict(
#         source=video_abs_path,
#         save=True,
#         project=os.path.abspath(os.path.join("..", "model-training", "runs", "detect")),
#         name=output_folder,
#         exist_ok=True
#     )

#     saved_dir = results[0].save_dir
#     raw_video_path = next((os.path.join(saved_dir, f) for f in os.listdir(saved_dir) if f.endswith((".avi", ".mp4"))), None)

#     if not raw_video_path:
#         raise FileNotFoundError("No output video found.")

#     converted_filename = f"output_{timestamp}.mp4"
#     converted_path = os.path.join(STATIC_DIR, converted_filename)

#     subprocess.run([
#         FFMPEG_PATH,
#         "-y",
#         "-i", raw_video_path,
#         "-vcodec", "libx264",
#         "-crf", "23",
#         converted_path
#     ], check=True)

#     return converted_filename

import cv2
import os
import csv
import subprocess
from datetime import datetime
from ultralytics import YOLO
import numpy as np
from bson import ObjectId
from app.extensions import mongo
from app.utils.email_utils import send_alert_email

# --- Paths ---
MODEL_PATH = os.path.join(os.path.dirname(__file__), "weights", "best.pt")

FFMPEG_PATH = r"C:\\ffmpeg-master-latest-win64-gpl-shared\\bin\\ffmpeg.exe"
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
LOG_PATH = os.path.join("logs", "zone_log.csv")

# --- Initialization ---
model = YOLO(MODEL_PATH)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

helmet_last_alert_time = None
helmet_cooldown_seconds = 60
last_alert_time = {}
zone_status = {}  # Make sure zone status is tracked globally
last_face_seen_time = datetime.now()
face_absent_alert_sent = False

# --- Create log directory ---
os.makedirs("logs", exist_ok=True)
if not os.path.exists(LOG_PATH):
    with open(LOG_PATH, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Time", "Zone", "Face_ID", "Helmet", "Event"])

# --- Utility ---
def get_zones_for_user(user_id):
    zones_cursor = mongo.db.zones.find({"user_id": ObjectId(user_id)})
    return {
        zone['zone_name']: {
            'x1': int(zone['x1']),
            'y1': int(zone['y1']),
            'x2': int(zone['x2']),
            'y2': int(zone['y2'])
        }
        for zone in zones_cursor
    }

def get_iou(boxA, boxB):
    xA, yA = max(boxA[0], boxB[0]), max(boxA[1], boxB[1])
    xB, yB = min(boxA[2], boxB[2]), min(boxA[3], boxB[3])
    interArea = max(0, xB - xA) * max(0, yB - yA)
    boxAArea = (boxA[2]-boxA[0]) * (boxA[3]-boxA[1])
    boxBArea = (boxB[2]-boxB[0]) * (boxB[3]-boxB[1])
    return interArea / float(boxAArea + boxBArea - interArea + 1e-6)

def point_in_zone(x, y, zone):
    return zone['x1'] <= x <= zone['x2'] and zone['y1'] <= y <= zone['y2']

def log_event(user_id, zone_name, face_id, helmet_status, event_type):
    try:
        print(f"[LOGGED] {event_type} | {zone_name} | {face_id} | {helmet_status}")
        mongo.db.detections.insert_one({
            "user_id": user_id,
            "zone": zone_name,
            "face_id": face_id,
            "helmet": helmet_status,
            "event": event_type,
            "timestamp": datetime.utcnow()
        })
    except Exception as e:
        print(f"[ERROR] Failed to log detection: {e}")

# --- Process Frame ---
def process_frame(frame, user=None):
    global helmet_last_alert_time, zone_status, last_face_seen_time, face_absent_alert_sent

    user_id = user
    
    if not user_id:
        print("[ERROR] user_id is None")
        return frame

    zones = get_zones_for_user(user_id)
    if not zones:
        print("[WARN] No zones found for user.")
        return frame

    timestamp = datetime.now()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 5)

    # ✅ Alert for no face detected for > 60 seconds
    if len(faces) == 0:
        time_since_last_face = (timestamp - last_face_seen_time).total_seconds()
        if time_since_last_face > 60 and not face_absent_alert_sent:
            print("[ALERT] No person detected for over 60 seconds.")
            send_alert_email(user=user_id, detections=["No Person Detected"], zones=list(zones.keys()))
            face_absent_alert_sent = True
    else:
        last_face_seen_time = timestamp
        face_absent_alert_sent = False

    results = model(frame)[0]
    helmet_boxes = [tuple(map(int, box.xyxy[0])) for box in results.boxes if results.names[int(box.cls[0])] == "helmet"]

    zone_occupied = {z: False for z in zones}
    helmet_violation = False
    unattended_zones = []

    for i, (x, y, w, h) in enumerate(faces):
        center_x, center_y = x + w // 2, y + h // 2
        face_id = f"Face_{i}"

        cv2.circle(frame, (center_x, center_y), 5, (255, 255, 255), -1)
        cv2.putText(frame, "Center", (center_x + 5, center_y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

        helmet_found = any(get_iou((x, y, x + w, y + h), hb) > 0.2 for hb in helmet_boxes)
        helmet_status = "Helmet" if helmet_found else "No Helmet"
        color = (0, 255, 0) if helmet_found else (0, 0, 255)

        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, f"{face_id} - {helmet_status}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        if not helmet_found:
            helmet_violation = True

        in_any_zone = False

        for zone_name, zone in zones.items():
            in_zone = point_in_zone(center_x, center_y, zone)
            key = (face_id, zone_name)

            if in_zone:
                in_any_zone = True
                zone_occupied[zone_name] = True
                if not zone_status.get(key):
                    log_event(user_id, zone_name, face_id, helmet_status, "Entered")
                    zone_status[key] = True
            elif zone_status.get(key):
                log_event(user_id, zone_name, face_id, helmet_status, "Exited")
                zone_status[key] = False

        if not in_any_zone:
            print(f"[SKIP] {face_id} not in any zone. No logging.")

    for zone_name, occupied in zone_occupied.items():
        if not occupied:
            last_time = last_alert_time.get(zone_name)
            if not last_time or (timestamp - last_time).total_seconds() > 60:
                unattended_zones.append(zone_name)
                print(f"[ALERT] Unattended zone: {zone_name}")
                log_event(user_id=user_id, zone_name=zone_name, face_id="None", helmet_status="None", event_type="Unattended")
                last_alert_time[zone_name] = timestamp
                z = zones[zone_name]
                cv2.rectangle(frame, (z["x1"], z["y1"]), (z["x2"], z["y2"]), (0, 0, 255), 2)

    if helmet_violation and (not helmet_last_alert_time or (timestamp - helmet_last_alert_time).total_seconds() > helmet_cooldown_seconds):
        send_alert_email(user=user_id, detections=["No Helmet"], zones=unattended_zones)
        helmet_last_alert_time = timestamp
    elif unattended_zones:
        print("[EMAIL] Sending unattended zone alert:", unattended_zones)
        send_alert_email(user=user_id, detections=[], zones=unattended_zones)

    for zone_name, coords in zones.items():
        cv2.rectangle(frame, (coords["x1"], coords["y1"]), (coords["x2"], coords["y2"]), (255, 255, 0), 2)
        cv2.putText(frame, zone_name, (coords["x1"], coords["y1"] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    return frame

# --- Image ---
def detect_image(image_path, user=None):
    frame = cv2.imread(image_path)
    processed = process_frame(frame, user=user)
    output_path = os.path.join(STATIC_DIR, "output.jpg")
    cv2.imwrite(output_path, processed)
    return output_path

# --- Video ---
def detect_video(video_path, user=None, output_folder="custom_video_output"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_abs_path = os.path.abspath(video_path)

    results = model.predict(
        source=video_abs_path,
        save=True,
        project=os.path.abspath(os.path.join("..", "model-training", "runs", "detect")),
        name=output_folder,
        exist_ok=True
    )

    saved_dir = results[0].save_dir
    raw_video_path = next((os.path.join(saved_dir, f) for f in os.listdir(saved_dir) if f.endswith((".avi", ".mp4"))), None)

    if not raw_video_path:
        raise FileNotFoundError("No output video found.")

    converted_filename = f"output_{timestamp}.mp4"
    converted_path = os.path.join(STATIC_DIR, converted_filename)

    subprocess.run([
        FFMPEG_PATH,
        "-y",
        "-i", raw_video_path,
        "-vcodec", "libx264",
        "-crf", "23",
        converted_path
    ], check=True)

    return converted_filename


