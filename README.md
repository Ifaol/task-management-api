# Task Management API

A production-oriented RESTful API for managing tasks, workspaces, and team collaboration with role-based access control.

This project is being developed as a backend capstone project to apply modern Python backend development concepts, including API design, database modeling, authentication, authorization, caching, background processing, testing, and containerization.

## Tech Stack

- **Python 3.12**
- **FastAPI**
- **Pydantic V2**
- **SQLAlchemy**
- **PostgreSQL**
- **Alembic**
- **JWT Authentication**
- **Redis**
- **Docker & Docker Compose**
- **uv**
- **Pytest**

## Core Features

### Authentication

- User registration
- Secure password hashing
- JWT-based authentication
- Protected API endpoints
- Authentication rate limiting

### Workspaces & RBAC

- Create workspaces
- Workspace membership
- Role-based access control
- Owner, editor, and viewer roles
- Permission-based FastAPI dependencies

### Task Management

- Create tasks
- View workspace tasks
- Update tasks
- Delete tasks
- Assign tasks to users
- Task status management
- Due dates

### Caching & Performance

- Redis task caching
- Cached task summaries
- Cache invalidation after mutations
- Authentication rate limiting with Redis

### Background Processing

- Welcome emails
- Notifications
- CSV task exports
- Asynchronous export processing

### Database

- PostgreSQL
- SQLAlchemy ORM
- Many-to-many workspace membership
- Alembic database migrations

### Development & Deployment

- Dockerized FastAPI application
- Dockerized PostgreSQL
- Dockerized Redis
- Docker Compose
- Automated testing
- Code quality tooling

## Project Structure

```text
task-management-api/
├── src/
│   └── task_management_api/
│       ├── main.py
│       ├── core/
│       ├── db/
│       ├── models/
│       ├── schemas/
│       ├── api/
│       ├── services/
│       ├── cache/
│       └── workers/
│
├── tests/
├── alembic/
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
├── .env
└── README.md
```

## Getting Started

### Prerequisites

Make sure the following are installed:

- Python 3.12+
- uv
- Git
- Docker
- Docker Compose

### Clone the Repository

```bash
git clone https://github.com/Ifaol/task-management-api.git
cd task-management-api
```

### Install Dependencies

The project uses `uv` for Python dependency and environment management.

```bash
uv sync
```

### Run the Development Server

```bash
uv run fastapi dev src/task_management_api/main.py
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

Alternative documentation:

```text
http://127.0.0.1:8000/redoc
```

## Environment Variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/taskdb

REDIS_URL=redis://localhost:6379/0

JWT_SECRET_KEY=change-me
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> Never commit `.env` or production secrets to Git.

## Database Migrations

Alembic will be used to manage database schema migrations.

Create a migration:

```bash
uv run alembic revision --autogenerate -m "migration description"
```

Apply migrations:

```bash
uv run alembic upgrade head
```

Rollback the latest migration:

```bash
uv run alembic downgrade -1
```

## Testing

Run the test suite with:

```bash
uv run pytest
```

## Code Quality

Run Ruff:

```bash
uv run ruff check .
```

Run MyPy:

```bash
uv run mypy src
```

## Docker

The final application will run using Docker Compose with:

```text
FastAPI
   │
   ├── PostgreSQL
   │
   └── Redis
```

Start the complete development environment:

```bash
docker compose up --build
```

Stop the environment:

```bash
docker compose down
```

## API Overview

### Authentication

```text
POST /auth/register
POST /auth/login
```

### Workspaces

```text
POST /workspaces/
POST /workspaces/{workspace_id}/members
```

### Tasks

```text
POST   /workspaces/{workspace_id}/tasks/
GET    /workspaces/{workspace_id}/tasks/
PUT    /workspaces/{workspace_id}/tasks/{task_id}
DELETE /workspaces/{workspace_id}/tasks/{task_id}
```

### Advanced Features

```text
GET  /workspaces/{workspace_id}/tasks/summary
POST /workspaces/{workspace_id}/tasks/export
```

## Workspace Roles

| Role   | Permissions                        |
| ------ | ---------------------------------- |
| Owner  | Full workspace and task management |
| Editor | Create and update tasks            |
| Viewer | View workspace tasks               |

## Development Roadmap

- [x] Initialize Python project with uv
- [x] Configure FastAPI
- [x] Initialize Git repository
- [x] Push project to GitHub
- [ ] Configure project architecture
- [ ] Configure PostgreSQL
- [ ] Configure SQLAlchemy
- [ ] Configure Alembic
- [ ] Implement database models
- [ ] Implement Pydantic schemas
- [ ] Implement user registration
- [ ] Implement JWT authentication
- [ ] Implement workspace management
- [ ] Implement RBAC
- [ ] Implement task CRUD
- [ ] Implement Redis caching
- [ ] Implement rate limiting
- [ ] Implement background tasks
- [ ] Implement CSV export
- [ ] Add automated tests
- [ ] Dockerize application
- [ ] Configure Docker Compose
- [ ] Final API documentation

## Project Goals

This project is intended to demonstrate practical understanding of:

- REST API design
- Python type hints
- Dependency injection
- Pydantic validation
- Relational database design
- ORM usage
- Database migrations
- JWT authentication
- Role-based access control
- Redis caching
- Rate limiting
- Background processing
- Automated testing
- Docker containerization
- Clean backend architecture

## License

This project is currently intended for educational and portfolio purposes.
