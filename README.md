# Manuzam  
**A Pattern-Based and Multi-Signal Approach for Failure Prediction in the Manufacturing Industry**

---

## Project Description

**Manuzam** is an intelligent failure prediction system designed to detect anomalies in industrial machinery using machine learning and multi-signal inputs like **audio** and **temperature** data.

It allows users to **train custom machine learning models** based on uploaded or recorded machine sounds and monitor real-time machine behavior. The system predicts mechanical faults by analyzing sound patterns and sensor data, supporting proactive maintenance and reducing unexpected downtimes.

---

## Key Features

- Upload or record machine audio for fault detection  
- Integrate temperature (and future environmental sensors) for enhanced prediction  
- Train and use custom ML models per machine  
- User feedback system: annotate predictions to improve future accuracy  
- Real-time predictions displayed on a modern frontend  
- Modular architecture with clean separation of frontend, backend, and ML logic  
- RESTful API for external integrations

---

## Use Case Scenarios

### 1. Custom Machine Monitoring
- User records sound data and trains a dedicated model.  
- The system listens and flags anomalies in real time.

### 2. Remote Fault Diagnosis
- Upload any machine’s sound recording.  
- The system returns a fault prediction based on the trained model.

### 3. Temperature-Sound Fusion
- Combines acoustic data with temperature readings for robust anomaly detection.

### 4. Fault Feedback Loop
- Users label false positives/negatives and submit the actual cause.  
- These inputs help refine the model through retraining.

---

## Tech Stack

| Layer        | Technology         |
|--------------|--------------------|
| Frontend     | Vue.js 3 + Vite     |
| Backend      | FastAPI (Python)    |
| ML Framework | Scikit-learn        |
| Optional IoT | ESP32 (Sensor Input)|

---

## Installation Guide

### Clone the Repository
```bash
git clone https://github.com/your-username/manuzam.git
cd manuzam
```

### Backend Setup (FastAPI + ML)

#### Navigate to the backend directory:
```bash
cd backend
```

#### Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

#### Install dependencies:
```bash
pip install -r requirements.txt
```

#### Create a .env file:
```env
# backend/.env
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=your-secret-key
```
You can also copy a template:
```bash
cp .env.example .env
```

#### Run the backend server:
```bash
uvicorn main:app --reload
```

By default, the backend runs at:  
[http://localhost:8000](http://localhost:8000)

---

### Frontend Setup (Vue.js + Vite)

#### Navigate to the frontend directory:
```bash
cd ../frontend
```

#### Install dependencies:
```bash
npm install
```

#### (Optional) Configure the API base URL:
Create a `.env` file in the frontend folder:
```env
# frontend/.env
VITE_API_BASE_URL=http://localhost:8000
```

#### Start the frontend development server:
```bash
npm run dev
```

By default, the frontend runs at:  
[http://localhost:5173](http://localhost:5173)

---

## How It Works

1. Upload or record an audio sample from a machine.  
2. The backend preprocesses and runs the audio through a trained model.  
3. The result (normal/faulty) is sent back to the frontend and displayed.  
4. Optionally, users can provide feedback about incorrect predictions.  
5. The system stores this data for future model retraining and improvement. 

---

## Future Enhancements

- Real-time IoT sensor integration (ESP32, temperature, vibration)  
- On-device ML (Edge deployment)  
- Dashboard with time series charts and logs  
- Support for additional sensor types (e.g., current, humidity)  
- Feedback loop with active learning for continuous model improvement

---

## License

This project is licensed under the MIT License.  
See [LICENSE](LICENSE) for details.

---

## Author

**Muhammad Zain ul Abideen**  
MSc Student, Université Jean Monnet & École des Mines de Saint-Étienne  
Personal project under academic supervision
