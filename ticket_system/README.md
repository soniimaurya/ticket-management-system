# Ticket Management System API

A production-ready REST API built with **FastAPI**, **SQLAlchemy**, and **SQLite** featuring JWT authentication, role-based access control, and an optional AI assistant.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| ORM | SQLAlchemy 2.x |
| Database | SQLite (swap to PostgreSQL via `DATABASE_URL`) |
| Auth | JWT via `python-jose` + `passlib[bcrypt]` |
| Validation | Pydantic v2 |
| AI Feature | Anthropic Claude API |

---

## Project Structure

```
ticket_system/
├── main.py                  # App entry point, middleware, router registration
├── models.py                # SQLAlchemy ORM models (User, Ticket)
├── schemas.py               # Pydantic request/response schemas
├── database.py              # DB engine, session, Base
├── core/
│   ├── config.py            # Settings loaded from .env
│   ├── security.py          # Password hashing, JWT creation/decoding
│   └── dependencies.py      # FastAPI dependency injection (auth guards)
├── routers/
│   ├── auth.py              # POST /auth/register, POST /auth/login
│   ├── tickets.py           # Full ticket CRUD for regular users
│   ├── admin.py             # Admin-only routes (all tickets + stats)
│   └── ai_assistant.py      # POST /ai/ask — natural language queries
├── services/
│   ├── auth_service.py      # Registration and login business logic
│   └── ticket_service.py    # Ticket CRUD, filtering, pagination, stats
├── requirements.txt
├── .env.example
└── README.md
```

---

## Setup & Run

### 1. Clone and create environment

```bash
git clone <your-repo>
cd ticket_system
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env — set SECRET_KEY and optionally ANTHROPIC_API_KEY
```

### 3. Run the server

```bash
uvicorn main:app --reload
```

Visit **http://localhost:8000/docs** for the interactive Swagger UI.

---

## API Reference

### Authentication

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/auth/register` | Register a new user | Public |
| POST | `/auth/login` | Login, receive JWT | Public |

### Tickets (User)

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/tickets/` | Create a ticket | Required |
| GET | `/tickets/` | List own tickets (filter/search/sort/paginate) | Required |
| GET | `/tickets/{id}` | Get ticket by ID | Required |
| PUT | `/tickets/{id}` | Update ticket fields | Required |
| PATCH | `/tickets/{id}/status` | Update ticket status only | Required |
| DELETE | `/tickets/{id}` | Delete ticket | Required |

### Admin

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/admin/tickets` | List ALL tickets | Admin only |
| GET | `/admin/stats` | Ticket and user statistics | Admin only |

### AI Assistant (Bonus)

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/ai/ask` | Natural language ticket query | Required |

---

## Query Parameters (GET /tickets/)

| Parameter | Type | Example | Description |
|---|---|---|---|
| `status` | enum | `open` | Filter by status |
| `priority` | enum | `high` | Filter by priority |
| `category` | enum | `bug` | Filter by category |
| `search` | string | `login error` | Search title & description |
| `sort_by` | string | `priority` | Field to sort by |
| `sort_order` | string | `asc` | `asc` or `desc` |
| `page` | int | `2` | Page number (default 1) |
| `page_size` | int | `20` | Results per page (max 100) |

---

## Roles & Permissions

| Action | User | Admin |
|---|---|---|
| Register / Login | ✅ | ✅ |
| Create ticket | ✅ | ✅ |
| View own tickets | ✅ | ✅ |
| View all tickets | ❌ | ✅ |
| Edit own tickets | ✅ | ✅ |
| Edit any ticket | ❌ | ✅ |
| Delete own tickets | ✅ | ✅ |
| Delete any ticket | ❌ | ✅ |
| Admin stats | ❌ | ✅ |
| AI assistant | ✅ | ✅ |

---

## Enums Reference

**Status:** `open` · `in_progress` · `resolved` · `closed`

**Priority:** `low` · `medium` · `high` · `critical`

**Category:** `bug` · `feature` · `support` · `other`

---

## Quick Start — Example Requests

### Register a user
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "email": "alice@example.com", "password": "secret123"}'
```

### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "secret123"}'
# Copy the access_token from the response
```

### Create a ticket
```bash
curl -X POST http://localhost:8000/tickets/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Login page broken", "description": "500 error on submit", "priority": "high", "category": "bug"}'
```

### Ask the AI assistant
```bash
curl -X POST http://localhost:8000/ai/ask \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"question": "Show all high priority open tickets"}'
```

---

## Create an Admin User

Register normally, then manually set the role in the DB (or register with `"role": "admin"` during development):

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "email": "admin@example.com", "password": "admin123", "role": "admin"}'
```

---

## AI Assistant Feature

Set `ANTHROPIC_API_KEY` in your `.env` file. The assistant retrieves all tickets visible to the current user and answers natural language questions about them.

Example questions:
- *"What is the status of ticket 3?"*
- *"Summarize ticket 12"*
- *"How many open high-priority bugs do we have?"*
- *"Which tickets were created this week?"*

---

## Switching to PostgreSQL

Change `DATABASE_URL` in `.env`:

```
DATABASE_URL=postgresql://user:password@localhost:5432/tickets_db
```

Install the driver:
```bash
pip install psycopg2-binary
```

No other code changes needed — SQLAlchemy handles the rest.

---

## Bonus Features Implemented

- ✅ Pagination (page + page_size on all list endpoints)
- ✅ Search (full-text search on title and description)
- ✅ Sorting (any field, asc/desc)
- ✅ Logging (request logging middleware + Python logging)
- ✅ AI/RAG ticket chatbot (POST /ai/ask)
