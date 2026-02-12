## Backend – HRMS Lite API

### Overview

This backend provides a minimal HRMS Lite API for:
- **Employee management** – add, list, and delete employees.
- **Attendance management** – mark attendance and view attendance records.
- **Dashboard metrics** – total employees, present today, and absent today.

It is built with **FastAPI**, **SQLAlchemy**, and a SQL database (PostgreSQL preferred, SQLite fallback).

### Tech Stack

- **Language**: Python 3.11+
- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Database**: PostgreSQL (recommended) or SQLite (default fallback)
- **Server**: Uvicorn

### Folder Structure

- `app/main.py` – FastAPI application factory, router registration, CORS setup.
- `app/core/config.py` – Centralized configuration using `BaseSettings` and environment variables.
- `app/db/session.py` – SQLAlchemy engine, `SessionLocal`, and `get_db` dependency.
- `app/db/base.py` – Imports all models so metadata is complete.
- `app/models/employee.py` – `Employee` ORM model with unique `employee_id`.
- `app/models/attendance.py` – `Attendance` ORM model with FK to employee and date/status fields.
- `app/schemas/employee.py` – Pydantic schemas for employee create/read/list.
- `app/schemas/attendance.py` – Pydantic schemas for attendance create/read/list and status enum.
- `app/routers/employee.py` – Employee CRUD endpoints.
- `app/routers/attendance.py` – Attendance mark + list endpoints.
- `app/routers/dashboard.py` – Dashboard summary endpoint.
- `app/services/` – Reserved for business logic/services (currently simple enough to keep in routers).

### Environment Variables

Configured via `.env` (see `.env.example`):

- **`DATABASE_URL`** (optional but recommended):
  - Full SQLAlchemy database URL string.
  - Example for PostgreSQL: `postgresql+psycopg2://user:password@localhost:5432/hrms_lite`
  - If omitted, the app falls back to `sqlite:///./hrms_lite.db` in the working directory.
- **`BACKEND_CORS_ORIGINS`** (optional):
  - Comma-separated list of allowed origins, e.g. `http://localhost:5173,https://hrms-lite.example.com`.
  - If left empty, all origins are allowed (development-friendly, not recommended for production).

### Running Locally

1. **Install Python dependencies**

   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Configure environment**

   ```bash
   cp .env.example .env
   # Adjust DATABASE_URL and BACKEND_CORS_ORIGINS as needed
   ```

   For quick local development, you can leave `DATABASE_URL` empty to use SQLite.

3. **Run the API server**

   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`.

### Database Setup

#### SQLite (default fallback)

If `DATABASE_URL` is not provided, the app uses:

```text
sqlite:///./hrms_lite.db
```

The database file `hrms_lite.db` will be created automatically in the backend working directory. Tables are created on application startup using `Base.metadata.create_all(bind=engine)`.

#### PostgreSQL (recommended for deployment)

1. Create a PostgreSQL database and user.
2. Set `DATABASE_URL` in `.env`, for example:

   ```text
   DATABASE_URL=postgresql+psycopg2://hrms_user:strong_password@localhost:5432/hrms_lite
   ```

3. Start the API. Tables will be created automatically on startup.

### REST Endpoints

Base prefix: `/api`

- **Employees**
  - `POST /api/employees` – Create employee.
  - `GET /api/employees?q=search` – List employees, optional free-text search.
  - `DELETE /api/employees/{employee_id}` – Delete employee by public `employee_id`.

- **Attendance**
  - `POST /api/attendance` – Mark attendance (`employee_id`, `attendance_date`, `status`).
  - `GET /api/attendance?employee_id=E123&date=2026-02-12` – List attendance, optional filter by employee and/or date.

- **Dashboard**
  - `GET /api/dashboard/summary` – Returns `total_employees`, `present_today`, `absent_today`.

All endpoints return **graceful error responses** using FastAPI `HTTPException` with appropriate HTTP status codes.

### CORS Configuration

CORS is enabled via `CORSMiddleware`:

- If `BACKEND_CORS_ORIGINS` is set, only those origins are allowed.
- If empty, `allow_origins=["*"]` is used for development convenience.

For production, set explicit origins, for example:

```text
BACKEND_CORS_ORIGINS=http://localhost:5173,https://hrms-lite-frontend.vercel.app
```

### Deployment Guide

#### Docker (Render / Railway friendly)

1. Build the image:

   ```bash
   cd backend
   docker build -t hrms-lite-backend .
   ```

2. Run the container locally:

   ```bash
   docker run -p 8000:8000 --env-file .env hrms-lite-backend
   ```

3. For Render/Railway:
   - Use this repo as the service source.
   - Set the **Dockerfile** path to `backend/Dockerfile` (or configure a root build with appropriate context).
   - Configure environment variables in the platform dashboard (`DATABASE_URL`, `BACKEND_CORS_ORIGINS`).
   - Expose port `8000` (the `PORT` env var is respected by Render/Railway but we set default `8000`).

#### Non-Docker Deployment

On a VM or traditional server:

1. Install Python and dependencies as in the local setup section.
2. Set environment variables (`DATABASE_URL`, `BACKEND_CORS_ORIGINS`).
3. Run via a process manager, e.g. `gunicorn` with Uvicorn workers:

   ```bash
   pip install gunicorn
   gunicorn -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
   ```

4. Put a reverse proxy (e.g. Nginx) in front if desired.

### Assumptions & Limitations

- **No authentication** – all endpoints are open; suitable for assignment/demo, not for production access control.
- **Single attendance record per employee per date** – enforced by a unique constraint.
- **Dashboard counts**:
  - `present_today` and `absent_today` count **only employees with an attendance record for today**.
  - Employees without a record for today are not counted as present or absent.
- **Services layer** – kept minimal. Logic is simple enough to reside in routers; can be refactored into `services/` if the domain grows.
- **Migrations** – automatic table creation is used instead of a migration tool (e.g. Alembic) to keep the implementation lightweight.

