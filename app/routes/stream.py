from flask import Blueprint, Response, request,jsonify
import cv2
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.detection import process_frame

stream_bp = Blueprint("stream", __name__)

# Global camera state
camera_url = None
cap = None


# @stream_bp.route('/set-camera', methods=['POST'])
# @jwt_required()
# def set_camera():
#     global cap, camera_url
#     data = request.get_json()
#     camera_url = data.get("camera_url")

#     if not camera_url:
#         return {"error": "Camera URL required"}, 400

#     cap = cv2.VideoCapture(camera_url)
#     if not cap.isOpened():
#         return {"error": "Failed to connect to camera"}, 500

#     return {"message": "Camera connected successfully"}, 200
@stream_bp.route('/set-camera', methods=['POST'])
@jwt_required()
def set_camera():
    global cap, camera_url
    data = request.get_json()
    camera_url = data.get("camera_url")

    if not camera_url:
        return jsonify({"error": "Camera URL required"}), 400

    try:
        cap = cv2.VideoCapture(camera_url)
        if not cap.isOpened():
            cap.release()  # Clean up if failed
            return jsonify({"error": "Failed to connect to camera. Please check the URL/device index."}), 500
    except Exception as e:
        return jsonify({"error": f"Exception while connecting to camera: {str(e)}"}), 500

    return jsonify({"message": "Camera connected successfully"}), 200


# @stream_bp.route('/video-feed')
# @jwt_required()
# def video_feed():
#     def gen_frames():
#         global cap
#         user_id = get_jwt_identity()  # 🔒 Extract user from token

#         while cap is not None and cap.isOpened():
#             success, frame = cap.read()
#             if not success:
#                 break

#             try:
#                 frame = process_frame(frame, user_id)  # 🔍 Process + Log with real user ID
#             except Exception as e:
#                 print(f"[ERROR] in process_frame: {e}")
#                 continue

#             _, buffer = cv2.imencode('.jpg', frame)
#             yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

#     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@stream_bp.route('/video-feed')
def video_feed():
    global cap

    user_id = request.args.get("user")  # ✅ Access request args here, in context

    if cap is None or not cap.isOpened():
        return jsonify({"error": "Camera is not connected"}), 400

    def gen_frames(user_id):
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break
            try:
                frame = process_frame(frame, user_id)
            except Exception as e:
                print(f"[ERROR] in process_frame: {e}")
                continue

            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    return Response(gen_frames(user_id), mimetype='multipart/x-mixed-replace; boundary=frame')


