# AssignmentTracker

A REST API for tracking assignments, built with **FastAPI**, **SQLModel** and **PostgreSQL**, and run with **Docker Compose**.

## Tech stack

- [FastAPI](https://fastapi.tiangolo.com/) – web framework
- [SQLModel](https://sqlmodel.tiangolo.com/) – data models / ORM
- PostgreSQL 16 – database
- Docker & Docker Compose – containers

## Data model

An `Assignment` has:

| Field        | Type     | Notes                                   |
|--------------|----------|-----------------------------------------|
| `id`         | int      | Primary key                             |
| `title`      | str      | 1–200 characters                        |
| `subject`    | str      | Up to 100 characters                    |
| `due_date`   | date     |                                         |
| `status`     | enum     | `pending` (default), `in_progress`, `done` |
| `notes`      | str      | Optional                                |
| `created_at` | datetime | Set automatically                       |

## Getting started

1. Create a `.env` file in the project root:

   ```env
   POSTGRES_USER=your_user
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=assignments
   DATABASE_URL=postgresql://your_user:your_password@db:5432/assignments
   ```

2. Start the database and API:

   ```bash
   docker compose up --build
   ```

3. Open the API at <http://localhost:8000> and the interactive docs at <http://localhost:8000/docs>.

## Project structure

```
.
├── backend/
│   ├── main.py           # FastAPI app and routes
│   ├── auth.py           # Password hashing and JWT auth
│   ├── models.py         # SQLModel models
│   ├── database.py       # Engine and session setup
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html
│   ├── signup.html
│   ├── home.html
│   ├── api.js
│   └── style.css
├── docker-compose.yml
└── .env
```

To run the backend without Docker: `cd backend && fastapi dev main.py`
