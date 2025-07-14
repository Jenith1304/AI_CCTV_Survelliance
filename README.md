# 🛡️ AI CCTV Surveillance System

An AI-powered CCTV surveillance system that detects safety violations such as no-helmet detection using YOLOv8. The application includes:

-  Live Stream CCTV Feed
-  Real-Time Helmet Detection (YOLOv8)
-  Zone detection
-  Authenticated User Access
-  Media Upload & Logs
-  Email Alert Configuration
-  Deployed on Render

 **Live App**: [https://ai-cctv-survelliance.onrender.com](https://ai-cctv-survelliance.onrender.com)

---

##  Project Structure

ai-cctv-surveillance/<br>
├── app/ # Flask backend app<br>
│ ├── routes/ # All API routes<br>
│ ├── static/ # React build moved here<br>
│ ├── detection.py # Helmet detection logic<br>
│ ├── main.py # Flask entrypoint<br>
│ └── ...<br>
├── cctv-dashboard/ # React frontend (Vite)<br>
├── requirements.txt # Backend dependencies<br>
├── README.md<br>

---
⚠️ Important Notice about Hosting<br>
⚠ Live stream & detection may not work reliably on Render's free hosting due to limited memory, compute, and timeout restrictions.<br>

If you face issues such as:<br>

❌ 502 Bad Gateway<br>
⚠️ Crashing video feed<br>
🕒 Long delays or camera connection errors<br>

👉 Please run the project locally by following the steps below for best performance and reliability.<br>

---

## ⚙ How to Run the Project Locally

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-cctv-surveillance.git
cd ai-cctv-surveillance

2. Install Python Dependencies
pip install -r requirements.txt

3. Add .env file in app/
# app/.env

CLOUD_NAME=your_cloudinary_cloud
CLOUD_API_KEY=your_cloudinary_key
CLOUD_API_SECRET=your_cloudinary_secret
JWT_SECRET_KEY=your_jwt_secret
SECRET_KEY=your_flask_secret
MONGO_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net/ai_cctv

4. Build React Frontend & Move to Backend Static

cd cctv-dashboard
npm install
npm run build
mkdir -p ../app/static
cp -r dist/* ../app/static/

5. Start Flask Backend
cd ..
python app/main.py
```

👨‍💻 Developer
Name: Jenith<br>
Enrollment No: 230173116007<br>
Tech Stack: Python, Flask, MongoDB, React (Vite), YOLOv8<br>
Email:minakanupanchal@gmail.com<br>
College:Vishwakarma Government Engineering College,Ahmedabad

💡 Tips for Using with CCTV Apps
Use an Android CCTV app like IP Webcam

Use its HTTP stream (e.g., http://192.168.1.x:8080/video)

Make it public with ngrok:
ngrok http 8080
Use the generated HTTPS URL + /video in the app.


