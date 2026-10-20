# Mental Health Support Web Application

A full-stack web application designed to facilitate mental health support through secure doctor-patient interactions, appointment management, real-time chat, prescription management, and AI-powered emotion detection.

## Features

- **Role-Based Authentication**: Separate interfaces for doctors and patients
- **Appointment Management**: Book, accept, reject, and manage appointments
- **Real-Time Chat**: Secure messaging between doctors and patients via AJAX polling
- **Prescription Management**: Create and view prescriptions with notes and recommended tests
- **Emotion Detection**: AI-powered emotion analysis using RoBERTa-based model
- **UPI Integration**: Display UPI IDs and generate QR codes for payments
- **Responsive Design**: Modern, clean UI with mobile-friendly layout

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning the repository)

### Installation

1. **Clone or download the repository**
   ```bash
   git clone <repository-url>
   cd MentalHealthSupport
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   # For standard web server / serverless deployment (lightweight):
   pip install -r requirements.txt

   # OR for full local PyTorch model inference & training:
   pip install -r requirements-local.txt
   ```

4. **Verify model files (optional for local PyTorch mode)**
   - When running locally with PyTorch, ensure `emotion_roberta_model` directory exists:
     - `config.json`
     - `model.safetensors`
     - `tokenizer_config.json`
     - `vocab.json`
     - `merges.txt`
     - `special_tokens_map.json`
     - `best_config.json`
   - *Note: In serverless environments (e.g., Vercel), the app automatically uses the free cloud Hugging Face Inference API for the RoBERTa GoEmotions model without needing local model files.*

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your browser and navigate to: `http://localhost:5000`
   - The application will automatically initialize the database on first run

## Requirements

- **Production / Vercel (`requirements.txt`)**:
  - Flask 3.0.0
  - Flask-CORS 4.0.0
  - Flask-Login 0.6.3
  - Flask-SQLAlchemy 3.1.1
  - Requests (>=2.28.0)
  - Gunicorn (>=21.2.0)

- **Local Machine / Model Training (`requirements-local.txt`)**:
  - PyTorch (>=2.0.0)
  - Transformers (>=4.30.0)
  - Pandas (>=2.0.0)
  - NumPy (>=1.24.0)
  - Scikit-learn (>=1.3.0)
  - tqdm (>=4.65.0)

## Usage

### For Patients

1. **Register**: Create an account with role "patient"
2. **Book Appointment**: Select a doctor and schedule an appointment
3. **View Appointments**: Check appointment status (pending/accepted/rejected)
4. **Chat**: Communicate with your doctor through the chat interface
5. **View Prescriptions**: Access prescriptions provided by your doctor
6. **Emotion Analysis**: Analyze emotional sentiment from text input

### For Doctors

1. **Register**: Create an account with role "doctor" and specialization
2. **Manage Appointments**: Accept or reject appointment requests
3. **Chat**: Communicate with patients
4. **Create Prescriptions**: Write prescriptions with notes and recommended tests
5. **View History**: Access appointment and prescription history

## Project Structure

```
MentalHealthSupport/
├── app.py                      # Main Flask application
├── step_inference.py           # Emotion detection model inference
├── requirements.txt            # Python dependencies
├── emotion_mapping.json        # Emotion label mappings
├── mental_health.db            # SQLite database (auto-generated)
├── emotion_roberta_model/      # Pre-trained emotion detection model
├── static/
│   ├── style.css               # Application styles
│   └── script.js               # Client-side JavaScript
├── templates/
│   ├── base.html               # Base template
│   ├── home.html               # Home page
│   ├── dashboard.html          # User dashboard
│   ├── chat.html               # Chat interface
│   ├── emotion.html            # Emotion detection page
│   ├── appointments_doctor.html # Doctor appointments view
│   ├── appointments_patient.html # Patient appointments view
│   ├── book_appointment.html   # Appointment booking
│   ├── prescriptions.html      # Doctor prescriptions view
│   ├── prescriptions_patient.html # Patient prescriptions view
│   └── auth/
│       ├── login.html          # Login page
│       └── register.html       # Registration page
└── training/                   # Training data and scripts
```

## Deployment Guide

### Option 1: Deploying to Vercel (Serverless)

This repository is pre-configured for seamless Vercel deployment with `vercel.json`, `api/index.py`, and `.vercelignore`.

1. **Push your code to GitHub** (or connect your repo in Vercel Dashboard).
2. **Import the repository into Vercel**.
3. **Configure Environment Variables** in Vercel Project Settings:
   - `FLASK_SECRET`: A secure random secret key (e.g. `openssl rand -hex 32`)
   - `HF_TOKEN` (Optional): Your Hugging Face user access token for high-rate-limit serverless emotion detection inference.
   - `DATABASE_URL` (Recommended for production): PostgreSQL connection string (from free hosts like Neon, Supabase, or Railway) to persist user accounts and appointments across serverless cold starts.
4. **Click Deploy**. Vercel will install the lightweight `requirements.txt` (< 30 MB bundle) and your app will be live immediately!

### Option 2: Deploying to Render / Railway / Fly.io (Container)

For running the full local PyTorch model on a persistent server:
- **Render**: Connect the repository and select **Web Service** (or use Blueprint with included `render.yaml`).
- **Railway / Fly.io / Docker**: The repository includes `Dockerfile` and `Procfile`. Simply deploy using Docker runtime with `gunicorn`.

## Configuration

### Environment Variables

- `FLASK_SECRET`: Secret key for Flask sessions (default: "change-me-in-prod"). **Change this in production!**
- `DATABASE_URL`: PostgreSQL connection string (e.g., `postgresql://user:pass@host:5432/db`). If not set, falls back to SQLite.
- `HF_TOKEN`: Hugging Face access token for cloud emotion detection inference.
- `HF_EMOTION_MODEL`: Hugging Face model repository ID (default: `"SamLowe/roberta-base-go_emotions"`).

### Database

The application supports both PostgreSQL and SQLite:
- If `DATABASE_URL` is configured, it connects to PostgreSQL.
- If not configured:
  - In local/container environments, it stores SQLite at `mental_health.db`.
  - In Vercel serverless environments, it routes SQLite to `/tmp/mental_health.db` to prevent read-only filesystem restrictions.

## Notes

- The emotion detection model requires the `emotion_roberta_model` directory with all model files
- First-time model loading may take a few moments
- Chat messages are polled every 3 seconds for real-time updates
- Appointments can be deleted, which automatically deletes related chats and prescriptions
- UPI QR codes are generated using an external API (qrserver.com)

## Contributing

This is a project for mental health support. Contributions and improvements are welcome!

## Acknowledgments

- RoBERTa model for emotion detection
- Flask framework
- All open-source contributors

---

For detailed documentation, see [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)
