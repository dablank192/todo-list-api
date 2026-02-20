# Todo List API

This project is for the [Todo List API](https://roadmap.sh/projects/todo-list-api) challenge on **roadmap.sh**.

The system provides a RESTful API that allows users to register, log in, and manage their personal todo lists with advanced features like pagination, filtering, and security.

## 🚀 Features

- **Authentication:**
  - User Registration and Login.
  - API endpoints secured with JWT (JSON Web Tokens).
- **Todo Management:**
  - Create, Read, Update, and Delete todos (CRUD).
- **Filtering & Pagination:**
  - Search todos by keywords.
  - List pagination (limit/offset).

## 🛠 Tech Stack

- **Language:** Python 3.x
- **Framework:** FastAPI
- **Database:** PostgresSQL
- **Authentication:** JWT

## ⚙️ Installation & Setup

Follow these steps to run the project locally:

### 1. Clone the repository
```bash
git clone https://github.com/dablank192/todo-list-api.git
cd todo-list-api
```

### 2. Create and activate Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory and add the necessary variables (example):
```env
SECRET_KEY=your_super_secret_key
DATABASE_URL=sqlite:///./todos.db
```

### 5. Run the application

**If using FastAPI:**
```bash
uvicorn main:app --reload
```

**If using Django:**
```bash
python manage.py migrate
python manage.py runserver
```

**If using Flask:**
```bash
flask run
```

## 📖 API Endpoints

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `POST` | `/user/register` | Register a new account | ❌ |
| `POST` | `/login` | Login to get Token | ❌ |
| `GET` | `/user/{id}` | Get a user | ✅ |
| `POST` | `/todos` | Create a new todo | ✅ |
| `GET` | `/todos` | Get list (supports ?page=1&limit=10) | ✅ |
| `GET` | `/todos/{id}` | Get todo details | ✅ |
| `PUT` | `/todos/{id}` | Update a todo | ✅ |
| `DELETE` | `/todos/{id}` | Delete a todo | ✅ |

---
