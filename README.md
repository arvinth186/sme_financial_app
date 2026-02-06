# SME Financial App

A powerful AI-driven financial analysis application designed for Small and Medium-sized Enterprises (SMEs). This platform provides in-depth financial insights, health scores, and credit risk assessments across multiple sectors including Agriculture, Manufacturing, Retail, Logistics, and E-commerce.

## 🚀 Features

- **Multi-Sector Analysis**: Specialized financial analysis for Agriculture, Manufacturing, Retail, Logistics, and E-commerce.
- **AI-Powered Insights**: Uses Large Language Models (Langchain + OpenAI/Groq) to generate human-readable explanations of financial health.
- **Financial Health Scoring**: automated calculation of health scores and status.
- **Credit Risk Assessment**: Evaluates creditworthiness based on financial metrics.
- **Interactive Dashboard**: Visualizes KPIs and trends using charts.
- **Recommendation Engine**: Suggests suitable financial products based on risk and health profiles.

## 🛠️ Tech Stack

### Backend (`/app`)

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - High-performance Python web framework.
- **Database**: PostgreSQL with [SQLAlchemy](https://www.sqlalchemy.org/) ORM.
- **Data Processing**: Pandas, OpenPyXL.
- **AI/LLM**: Langchain, OpenAI/Groq.
- **Authentication**: JWT (JSON Web Tokens).

### Frontend (`/frontend`)

- **Framework**: [React](https://react.dev/) with [Vite](https://vitejs.dev/).
- **Language**: TypeScript.
- **Charting**: Recharts.
- **HTTP Client**: Axios.
- **PDF Generation**: jsPDF.

## 📂 Project Structure

```bash
sme_financial_app/
├── app/                # Backend application code (FastAPI)
│   ├── models/         # Database models
│   ├── routes/         # API endpoints
│   ├── services/       # Business logic & AI services
│   ├── database/       # DB connection & sessions
│   └── main.py         # Entry point
├── frontend/           # Frontend application code (React)
│   ├── src/            # Source code
│   └── package.json    # Frontend dependencies
├── create_tables.py    # Script to initialize database tables
└── requirements.txt    # Backend dependencies
```

## ⚡ Getting Started

### Prerequisites

- Python 3.10+
- Node.js & npm
- PostgreSQL Database

### 1. Backend Setup

1.  Navigate to the project root.
2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Configure Environment Variables:
    - Create a `.env` file in the `app/` directory (or root, depending on config).
    - Add your Database URL, Secret Keys, and API Keys (OpenAI/Groq).
5.  Initialize the Database:
    ```bash
    python create_tables.py
    ```
6.  Start the Backend Server:
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will be available at `http://localhost:8000`. API Docs at `http://localhost:8000/docs`.

### 2. Frontend Setup

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the Development Server:
    ```bash
    npm run dev
    ```
    The application will run at `http://localhost:5173`.

## 🌐 Deployment

The application is designed to be deployed with separate backend and frontend services.

- **Backend**: Can be deployed on platforms like Render, Railway, or AWS.
- **Frontend**: Optimized for Vercel, Netlify, or any static site host.

