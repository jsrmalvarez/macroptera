# CRUD Application

A full-stack CRUD (Create, Read, Update, Delete) application with:
- Frontend: React with Chakra UI components
- Backend: Python FastAPI with SQLAlchemy ORM
- Database: MariaDB (Dockerized)

## Project Structure

```
.
├── backend/               # Python FastAPI backend
│   ├── app/               # Application code
│   │   ├── core/          # Core functionality
│   │   ├── models/        # SQLAlchemy models
│   │   ├── routers/       # API endpoints
│   │   └── schemas/       # Pydantic schemas
│   └── tests/             # Pytest test files
├── frontend/              # React frontend
│   ├── public/            # Public assets
│   └── src/               # React source code
│       └── components/    # React components
└── docker/                # Docker configuration
    ├── docker-compose.yml # Docker compose config
    ├── backend.Dockerfile # Backend Docker config
    └── frontend.Dockerfile # Frontend Docker config
```

## Prerequisites

- Docker and Docker Compose
- Node.js and npm (for local frontend development)
- Python 3.11+ (for local backend development)

## Running with Docker

1. Start all services using Docker Compose:

```bash
cd docker
docker-compose up
```

This will start three containers:
- MariaDB database on port 3306
- Backend API on port 8000
- Frontend React app on port 3000

2. Access the application at http://localhost:3000

## Local Development

### Backend

1. Create a virtual environment:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the FastAPI server:

```bash
uvicorn app.main:app --reload
```

4. Access the API documentation at http://localhost:8000/docs

### Frontend

1. Install dependencies:

```bash
cd frontend
npm install
```

2. Start the development server:

```bash
npm start
```

3. Access the app at http://localhost:3000

## Features

- Create, read, update and delete items
- Clean and responsive UI with Chakra UI
- RESTful API with FastAPI
- Database ORM with SQLAlchemy
- Containerized database with MariaDB
- Complete test suite with pytest

## API Endpoints

- `GET /api/items/`: List all items
- `POST /api/items/`: Create new item
- `GET /api/items/{id}`: Get a specific item
- `PUT /api/items/{id}`: Update a specific item
- `DELETE /api/items/{id}`: Delete a specific item