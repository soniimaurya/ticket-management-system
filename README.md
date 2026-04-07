# 🎫 Ticket Management System API

A powerful **Ticket Management System** built using **FastAPI** that allows users to create, manage, and track support tickets efficiently.

---

## 🚀 Features

* 👤 User Authentication (JWT-based login/register)
* 🎟️ Create, update, delete tickets
* 🔍 Filter, search, sort, and paginate tickets
* 👨‍💼 Admin dashboard & statistics
* 🔐 Role-based access control (Admin/User)
* ⚡ Fast and scalable API with FastAPI
* 🤖 AI Assistant support (optional module)

---

## 🛠️ Tech Stack

* **Backend:** FastAPI
* **Database:** SQLite (can be upgraded to PostgreSQL/MySQL)
* **ORM:** SQLAlchemy
* **Authentication:** JWT (python-jose)
* **Password Hashing:** Passlib (bcrypt)

---

## 📂 Project Structure

```
ticket_system_project/
│
├── ticket_system/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── dependencies.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── tickets.py
│   │   ├── admin.py
│   │   └── ai_assistant.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   └── ticket_service.py
│
├── tickets.db
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/ticket-system-project.git
cd ticket-system-project
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

(If no requirements.txt, install manually:)

```bash
pip install fastapi uvicorn sqlalchemy python-jose passlib[bcrypt] python-multipart
```

---

## ▶️ Run the Application

```bash
uvicorn ticket_system.main:app --reload
```

App will run on:
👉 http://127.0.0.1:8000

---

## 📄 API Documentation

* Swagger UI: http://127.0.0.1:8000/docs
* ReDoc: http://127.0.0.1:8000/redoc

---

## 🔐 Authentication

* Uses **JWT tokens**
* First register → then login → get token
* Use token in headers:

```
Authorization: Bearer <your_token>
```

---

## 📊 API Endpoints

### Auth

* `POST /auth/register`
* `POST /auth/login`

### Tickets

* `POST /tickets/`
* `GET /tickets/`
* `GET /tickets/{id}`
* `PUT /tickets/{id}`
* `DELETE /tickets/{id}`

### Admin

* `GET /admin/stats`

---

## 📌 Future Improvements

* ✅ Frontend (React / Next.js)
* ✅ Email notifications
* ✅ File attachments in tickets
* ✅ Deployment (AWS / Render)

---

## 🤝 Contributing

Feel free to fork this repo and contribute!

---

## 📜 License

This project is open-source and available under the MIT License.

---

## 👨‍💻 Author

**Soni Maurya**

---

⭐ If you like this project, give it a star on GitHub!
