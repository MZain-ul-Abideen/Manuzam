# Manuzam

**A Pattern-Based and Multi-Signal Approach for Failure Prediction in the Manufacturing Industry**

---

## Project Description

**Manuzam** is an intelligent failure prediction system designed to detect anomalies in industrial machinery using machine learning and multi-signal inputs, such as audio and sensor data.

The system allows users to **train custom machine learning models** based on recorded or uploaded machine sounds and monitor real-time machine performance. It helps predict mechanical failures by analyzing sound patterns and environmental data, enabling proactive maintenance and reducing downtime.

---

## Key Features

- Upload or capture machine audio for anomaly detection  
- Integrate temperature (and future sensors) for enhanced fault prediction  
- Train custom ML models for different machines (flexible approach)  
- Users can mark detected faults and specify their causes to improve future predictions  
- Real-time results and statistics via a modern frontend  
- Modular design: backend, frontend, and ML pipeline are cleanly separated  
- REST API for easy integration and future expansion  

---

## Use Case Scenarios

1.**Custom Machine Monitoring**
   - User records machine sounds and trains a model.
   - Model is used to detect faults by analyzing real-time sound from the machine.

2.**Remote Diagnosis**
   - User uploads an audio file from any machine.
   - The system detects whether it's operating normally or has issues.

3.**Temperature-Sound Fusion**
   - Combine temperature readings and acoustic patterns for robust anomaly detection.

4.**Fault Feedback Loop**
   - Users can review detected faults and annotate them with the actual cause.
   - The system uses this feedback to enhance future model performance.

---

## Tech Stack

| Layer          | Technology                |
|----------------|---------------------------|
| Frontend       | Vue.js 3 + Vite           |
| Backend        | FastAPI (Python)          |
| ML Framework   | Scikit-learn |
| (Optional) IoT | ESP32      |

---

## How to Run the Project

### Prerequisites

- Python 3.12+
- Node.js 18+

---

### Future Enhancements
- Real-time IoT sensor integration (e.g., ESP32)
- Edge deployment of ML models on microcontrollers
- Visualization dashboard with time series and logs
- Support for vibration, current, or humidity sensors
- User feedback loop integration with active learning

---

### License
This project is licensed under the MIT License. See LICENSE for more info.

---

### Author
Muhammad Zain ul Abideen

MSc Student, Université Jean Monnet & École des Mines de Saint-Étienne

Personal project under supervision