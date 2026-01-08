# FastAPI Social Media API

A RESTful API built with FastAPI that demonstrates core backend development concepts including user authentication, database operations, and a voting system.

## What This Project Does

This is a social media backend where users can:
- Create an account and log in
- Create, read, update, and delete posts
- Vote (like) on posts
- View posts with their vote counts

## Tech Stack

- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Database
- **SQLAlchemy** - Database ORM (Object Relational Mapper)
- **Alembic** - Database migrations
- **JWT** - Secure authentication tokens
- **Pytest** - Testing framework

## Project Structure

```
ORM_lesson2/
├── app/
│   ├── main.py           # Main application file
│   ├── models.py         # Database models (User, Post, Vote)
│   ├── schemas.py        # Data validation
│   ├── database.py       # Database connection
│   ├── oauth2.py         # Authentication logic
│   └── routers/          # API endpoints
│       ├── auth.py       # Login
│       ├── post.py       # Post operations
│       ├── user.py       # User operations
│       └── vote.py       # Voting
├── tests/                # Test files
├── alembic/              # Database migration files
└── requirements.txt      # Python dependencies
```

## Setup Instructions

### 1. Install Requirements

```bash
pip install -r requirements.txt
```

### 2. Setup Database

Create a PostgreSQL database and configure your `.env` file:

```env
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=fastapi_learn
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
SECRET_KEY=your_secret_key
ALGORITHM=HS256
EXPIRE_IN=60
```

### 3. Run Migrations

```bash
alembic upgrade head
```

### 4. Start the Server

```bash
uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs to see the interactive API documentation.

## API Endpoints

### Authentication
- `POST /users` - Create a new account
- `POST /login` - Login and get access token

### Posts (requires login)
- `GET /posts` - Get all posts
- `GET /posts/{id}` - Get a specific post
- `POST /posts` - Create a new post
- `PUT /posts/{id}` - Update your post
- `DELETE /posts/{id}` - Delete your post

### Votes (requires login)
- `POST /vote` - Vote on a post (use direction: 1 to like, 0 to remove like)

### Users
- `GET /users/{id}` - Get user information

## Database Schema

The app uses three main tables:

**Users** - Stores user accounts
- id, username, email, password, created_at

**Posts** - Stores user posts
- id, title, content, published, rating, created_at, user_id

**Votes** - Stores post likes
- post_id, user_id (combination is unique)

## Running Tests

```bash
pytest
```

Tests cover:
- User registration and authentication
- Creating, reading, updating, and deleting posts
- Voting functionality
- Authorization checks

## Docker Deployment

Build and run with Docker:

```bash
docker build -t fastapi-app .
docker run -p 8000:8000 --env-file .env fastapi-app
```

## What You'll Learn

This project demonstrates:
- Building REST APIs with FastAPI
- Database design and relationships
- User authentication with JWT tokens
- Password hashing for security
- Database migrations with Alembic
- Writing tests for APIs
- Deploying with Docker

---

**API Documentation**: Once running, visit `/docs` for interactive API documentation where you can test all endpoints.
