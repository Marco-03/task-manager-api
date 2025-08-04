# 🗂️ Task Manager API

A secure and modern REST API for managing personal tasks, built with **Flask**, **JWT**, and **SQLAlchemy**. Designed as a full-stack project for learning, testing, and extending.

---

## 🔧 Features

- ✅ User registration and authentication (`/signup`, `/login`)
- ✅ JWT-protected routes
- ✅ Full CRUD for tasks (Create, Read, Update, Delete)
- ✅ Task ownership per user
- ✅ Clean code structure (`models`, `routes`, `extensions`)
- ✅ Ready for frontend integration (React)

---

## 📁 Project Structure
```
backend/
├── app.py # App entrypoint
├── extensions.py # DB & JWT init
├── models.py # SQLAlchemy models
├── routes.py # Auth + task routes
├── requirements.txt # Dependencies
├── .gitignore # Excludes venv, db, etc.
```

---

## 🧪 API Endpoints

### 🔐 Auth

| Method | Endpoint   | Description       |
|--------|------------|-------------------|
| POST   | `/signup`  | Create user       |
| POST   | `/login`   | Get JWT token     |

### ✅ Tasks (JWT Protected)

| Method | Endpoint        | Description         |
|--------|------------------|---------------------|
| GET    | `/tasks`         | List user tasks     |
| GET    | `/tasks/<id>`    | Get single task     |
| POST   | `/tasks`         | Create task         |
| PUT    | `/tasks/<id>`    | Update task         |
| DELETE | `/tasks/<id>`    | Delete task         |

➡️ Use `Authorization: Bearer <token>` header for protected routes.

---

## ▶️ Getting Started

1. Clone the repo
2. Create virtualenv:
   ```bash
   python -m venv venv
   source venv/bin/activate  # on Windows: venv\Scripts\activate
3. Install dependencies:
    ```
    pip install -r requirements.txt

4. Run the app:
    ```
    python app.py
   
---
## ⚙️ Tech Stack

    Backend: Flask, SQLAlchemy, JWT, SQLite

    Security: Password hashing, route protection

    Testing: Postman


## 👨‍💻 Author

Marco-Antonio Luchian  
LinkedIn https://www.linkedin.com/in/marco-luchian-46293a244/