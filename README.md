# SME Financial App

A powerful FastAPI-based financial analysis and health scoring application designed for Small and Medium Enterprises (SMEs) across various industries.

## 🚀 Application Overview

The **SME Financial App** provides detailed financial insights, health scores, and credit risk assessments for businesses in the following sectors:

- **Agriculture**
- **Manufacturing**
- **Retail**
- **Logistics**
- **E-commerce**

It leverages AI (Large Language Models) to generate natural language explanations of financial metrics and recommends suitable financial products based on the business's health profile.

## ✨ Key Features

- **Financial Metrics Analysis**: Calculates profit margins, revenue trends, inventory ratios, and efficiency metrics from uploaded data.
- **Health Scoring**: specific algorithms to score business health (0-100) based on industry standards.
- **Credit Risk Assessment**: Categorizes credit risk (Low, Medium, High) derived from health scores.
- **AI-Powered Insights**: Uses LangChain (with Groq or OpenAI) to interpret financial data and provide actionable advice in multiple languages.
- **Product Recommendations**: Suggests financial products (loans, insurance, etc.) tailored to the business's risk profile.
- **Interactive Dashboard**: Endpoints to retrieve aggregated KPIs and historical analysis records.
- **Secure Authentication**: User management and authentication flows.
- **Data Templates**: Downloadable CSV templates for each industry to ensure correct data formatting.
- **Excel Support**: Upload and analyze data using both `.csv` and `.xlsx` formats.

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: SQLAlchemy (ORM)
- **Data Processing**: Pandas, OpenPyXL
- **AI/LLM**: LangChain, ChatGroq, ChatOpenAI
- **Server**: Uvicorn / Gunicorn

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository_url>
cd sme_financial_app
```

### 2. Set up a Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configuration

Create a `.env` file in the root directory and add your configuration variables:

```ini
DATABASE_URL=sqlite:///./sql_app.db # or your preferred DB connection string
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# LLM Configuration (Choose 'groq' or 'openai')
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key
# OPENAI_API_KEY=your_openai_api_key
MODEL_NAME=llama3-8b-8192 # or gpt-4o, etc.
TEMPERATURE=0.5
```

### 5. Initialize the Database

Run the script to create necessary tables:

```bash
python create_tables.py
```

## 🚀 Running the Application

### Development Mode

Start the development server with hot reload:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### Production Mode

Use the provided start script or run with Gunicorn:

```bash
# Using the script (ensure permissions are set: chmod +x start.sh)
./start.sh

# Or manually
gunicorn -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:10000
```

## 📚 API Documentation

Once the server is running, you can access the interactive API usage documentation at:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### New Endpoints

- **Download Templates**: `GET /templates/{industry}` (e.g., `/templates/retail`) to download a CSV template with the required columns.

## 📂 Project Structure

```
sme_financial_app/
├── app/
│   ├── auth/           # Authentication logic
│   ├── database/       # DB connection and dependency injection
│   ├── llm/            # LLM factory and configuration
│   ├── models/         # SQLAlchemy models (Agriculture, Retail, etc.)
│   ├── routes/         # API routes (including templates)
│   ├── services/       # Core business logic (analysis, scoring, credit)
│   └── main.py         # Application entry point
├── create_tables.py    # Database initialization script
├── requirements.txt    # Project dependencies
├── start.sh            # Production startup script
└── README.md           # Project documentation
```
