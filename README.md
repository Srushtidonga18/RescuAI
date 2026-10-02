# 🚨 RescuAI: Generative AI-Powered Emergency SOS Aggregator & Disaster Triage System

![RescuAI Banner](https://img.shields.io/badge/RescuAI-Disaster%20Triage-red?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google)

**RescuAI** is a centralized Generative AI-powered emergency management system designed to streamline crisis response. During natural disasters, control rooms are flooded with unstructured distress messages. RescuAI intelligently prioritizes, deduplicates, and triages these requests for Emergency Responders.

---

##  Key Features

- **Multimodal AI Triage:** Ingests raw text and voice messages, using Google Gemini AI to extract urgency, location, medical needs, and victim counts.
- **Offline Fallback Engine:** A robust, custom Regex-based NLP engine ensures the system continues to generate dispatch orders even if internet connectivity or the AI API fails.
- **Smart Spatial Deduplication:** Groups duplicate SOS requests within a 500-meter radius (using the Haversine formula) to prevent redundant dispatching.
- **AI Spam Detection:** Automatically flags and filters out non-emergency, troll, or commercial spam messages.
- **Real-Time Responder Dashboard:** A modern React.js interface for dispatchers to view a prioritized queue, manually assign rescue teams (NDRF/SDRF), and track inventory.
- **First-Aid AI Chatbot:** An intelligent assistant providing citizens with immediate, life-saving medical guidance (e.g., CPR, burns, snake bites) while they wait for help.

---

## 🏗️ System Architecture

1. **Frontend (React.js + Tailwind CSS):**
   - **Citizen SOS Portal:** For public users to send distress signals.
   - **Responder Dashboard:** Authenticated command center for dispatchers.
2. **Backend (FastAPI + SQLite):**
   - RESTful API handling authentication (JWT), SOS routing, and inventory logic.
3. **Intelligence Layer (Google Gemini / Offline NLP):**
   - Processes unstructured data into structured JSON Dispatch Cards.

---

## Technology Stack

- **Backend:** Python 3.10+, FastAPI, Uvicorn, SQLAlchemy 2.0 (ORM)
- **Frontend:** React.js (Vite), Tailwind CSS, Lucide React
- **AI/ML:** Google Gemini 1.5/3.8 Flash SDK
- **Database:** SQLite (Development)
- **Security:** Passlib, Bcrypt, JWT Tokens

---

## How to Run Locally

### 1. Backend Setup
\\\ash
# Navigate to the backend directory
cd backend

# Activate Virtual Environment (Windows)
.\venv\Scripts\Activate.ps1

# Install Dependencies
pip install -r requirements.txt

# Start the FastAPI Server (Port 8000)
python -m uvicorn backend.app.main:app
\\\

### 2. Frontend Setup
\\\ash
# Open a new terminal and navigate to frontend
cd frontend

# Install Node modules
npm install

# Start the Vite Development Server (Port 5173)
npm run dev
\\\

### 3. Environment Variables
Ensure a .env file exists in ackend/.env with your Google Gemini API key:
\\\env
GEMINI_API_KEY="AIzaSyYourKeyHere..."
SECRET_KEY="your-secret-key"
\\\

---
*Built to save lives, milliseconds at a time.*
