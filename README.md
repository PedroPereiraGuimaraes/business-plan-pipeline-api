# Business Plan Pipeline API

A professional backend for the Business Plan Pipeline SaaS, built with FastAPI, Python 3.11+, and PostgreSQL (Supabase compatible).

## 🚀 Features

- **Authentication**: Secure user registration and login with JWT and bcrypt.
- **Project Management**: Create and manage multiple business plan projects.
- **Onboarding**: Step-by-step onboarding for each project to gather business details.
- **AI Plan Generation**: Automated generation of business plans.
- **Consulting**: Request expert consulting with automated scheduling and Google Meet link generation.
- **Email Notifications**: Customized HTML email templates using Jinja2.
- **Scalable Architecture**: Modular design using Service Layer pattern and centralized API routing.
- **Automated Migrations**: Database schema updates automatically on startup.

## 🛠️ Tech Stack

- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Database**: PostgreSQL (via SQLAlchemy 2.0 & Alembic) / Supabase
- **Validation**: Pydantic v2
- **Templating**: Jinja2 (for emails)

## 📂 Project Structure

```
business-plan-pipeline-api/
├── alembic/              # Database migration scripts
├── app/
│   ├── api/              # API Router configuration
│   ├── auth/             # Authentication & User module
│   ├── consulting/       # Consulting requests module
│   ├── core/             # Core functionality (config, security, email)
│   ├── db/               # Database connection & models
│   ├── onboarding/       # Project onboarding module
│   ├── plans/            # Business plan generation module
│   ├── projects/         # Project management module
│   ├── templates/        # HTML templates for emails
│   ├── config.py         # Application configuration
│   └── main.py           # Application entry point
├── .env                  # Environment variables (gitignored)
├── alembic.ini           # Alembic configuration
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## ⚙️ Configuration

All configuration is managed via environment variables in a `.env` file. **No sensitive data is hardcoded.**

### Environment Variables

Copy `.env.example` to `.env` and configure:

```ini
# General
PROJECT_NAME="Business Plan Pipeline"
API_V1_STR="" # Leave empty to serve from root /

# Database (Recommended: Use DATABASE_URL)
DATABASE_URL=postgresql://user:password@host:port/dbname

# Legacy Database Config (Optional if DATABASE_URL is set)
POSTGRES_SERVER=db.example.com
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=app_db

# Security
SECRET_KEY=your_super_secret_key_change_me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS (Comma separated list)
BACKEND_CORS_ORIGINS=["http://localhost","http://localhost:3000","https://app.businessplanpipeline.com"]

# Email Settings
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password
MAIL_FROM=noreply@businessplanpipeline.com
MAIL_PORT=587
MAIL_SERVER=smtp.example.com
MAIL_FROM_NAME="Business Plan Pipeline"
MAIL_STARTTLS=True
MAIL_SSL_TLS=False
USE_CREDENTIALS=True
VALIDATE_CERTS=True
```

## 📦 Installation & Running

### Prerequisites
- Python 3.11+
- PostgreSQL database (or Supabase project)

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd business-plan-pipeline-api
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**:
   Create a `.env` file based on the example above and fill in your database credentials.

### Running the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

The application will:
1. Load configuration from `.env`.
2. **Automatically run database migrations** to ensure your schema is up to date.
3. Start the API server at `http://127.0.0.1:8000`.

## 🔗 API Documentation

Once running, access the interactive API docs:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 🗄️ Database Migrations

While migrations run automatically on startup, you can also manage them manually using Alembic:

- **Create a new migration** (after changing models):
  ```bash
  alembic revision --autogenerate -m "Description of changes"
  ```

- **Apply migrations manually**:
  ```bash
  alembic upgrade head
  ```
