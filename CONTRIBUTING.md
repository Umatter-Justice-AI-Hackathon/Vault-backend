# Contributing to Umatter Backend

Thank you for your interest in contributing! This guide will help you get set up for local development.

## Prerequisites

- Python 3.12
- PostgreSQL 14+
- Ollama (with llama3.1:8b model)
- Docker (for containerized development)
- [uv](https://github.com/astral-sh/uv) (Python package installer)

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/umatter-backend.git
cd umatter-backend
```

### 2. Set Up Python Environment

```bash
# Create virtual environment with Python 3.12
uv venv --python 3.12

# Activate the virtual environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows

# Install dependencies
uv pip install -r requirements.txt
uv pip install -r requirements-dev.txt
```

### 3. Set Up Database

```bash
# Create PostgreSQL database
createdb umatter

# Copy environment file and configure
cp .env.example .env
# Edit .env with your database credentials
```

### 4. Run Database Migrations

```bash
# Initialize Alembic (only needed once)
# alembic init alembic  # Already done

# Run migrations
alembic upgrade head
```

### 5. Start Ollama

```bash
# Start Ollama service
ollama serve

# In another terminal, ensure model is available
ollama pull llama3.1:8b
```

### 6. Run the Application

```bash
# Development mode with auto-reload
.venv/bin/uvicorn app.main:app --reload

# Or if you've activated the virtual environment:
# source .venv/bin/activate
# uvicorn app.main:app --reload

# The API will be available at:
# - http://localhost:8000
# - Docs: http://localhost:8000/api/v1/docs
```

## Docker Development

### Build Docker Image Locally

```bash
# Build the image
docker build -t umatter-backend:local .

# Run the container
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:password@host.docker.internal:5432/umatter" \
  -e OLLAMA_BASE_URL="http://host.docker.internal:11434" \
  umatter-backend:local
```

### Using Docker Compose (Coming Soon)

```bash
# Start all services (app, database, ollama)
docker-compose up

# Stop all services
docker-compose down
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_main.py -v

# Run tests matching a pattern
pytest -k "test_health"
```

## Code Quality

### Formatting

```bash
# Format code with Black
black app/ tests/

# Check formatting without changes
black --check app/ tests/
```

### Linting

```bash
# Lint with Ruff
ruff check app/ tests/

# Auto-fix issues
ruff check --fix app/ tests/
```

### Type Checking

```bash
# Run mypy type checker
mypy app/
```

### Run All Quality Checks

```bash
# Format, lint, and test
black app/ tests/ && \
ruff check --fix app/ tests/ && \
mypy app/ && \
pytest
```

## Database Migrations

### Create a New Migration

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Description of changes"

# Review the generated migration file in alembic/versions/

# Apply the migration
alembic upgrade head
```

### Rollback a Migration

```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>

# Rollback all migrations
alembic downgrade base
```

## GitHub Actions

The project uses GitHub Actions for CI/CD:

### Docker Image Build

On push to `main`, `develop`, or `draft-app` branches:
1. Builds Docker image
2. Pushes to GitHub Container Registry (ghcr.io)
3. Tags with branch name and SHA

### Image Naming Convention

- `ghcr.io/your-org/umatter-backend:main` - Latest main branch
- `ghcr.io/your-org/umatter-backend:develop` - Latest develop branch
- `ghcr.io/your-org/umatter-backend:draft-app-<sha>` - Specific commit
- `ghcr.io/your-org/umatter-backend:v1.0.0` - Version tags

### Pull Docker Image

```bash
# Login to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Pull image
docker pull ghcr.io/your-org/umatter-backend:main
```

## Project Structure

```
umatter-backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application entry point
│   ├── config.py         # Configuration management
│   ├── database.py       # Database setup and session management
│   ├── models.py         # SQLAlchemy ORM models
│   ├── schemas.py        # Pydantic request/response schemas
│   └── api/              # API route handlers (to be created)
├── tests/
│   ├── conftest.py       # Test fixtures and configuration
│   └── test_*.py         # Test files
├── alembic/              # Database migrations
├── .github/
│   └── workflows/        # GitHub Actions workflows
├── Dockerfile
├── requirements.txt
├── pyproject.toml        # Python project configuration
└── README.md
```

## Environment Variables

Required for local development (copy from `.env.example`):

```bash
# Database
DATABASE_URL=postgresql://localhost:5432/umatter

# OAuth (get from provider consoles)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
MICROSOFT_CLIENT_ID=your_microsoft_client_id
MICROSOFT_CLIENT_SECRET=your_microsoft_client_secret

# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# App
FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development
```

## Deployment to Render

See [RENDER_SETUP.md](RENDER_SETUP.md) for detailed deployment instructions.

Quick summary:
1. Create PostgreSQL database on Render
2. Create Web Service on Render
3. Connect to GitHub repository
4. Set environment variables
5. Render will automatically build and deploy using Dockerfile

## Getting Help

- Check existing issues on GitHub
- Review the [README.md](README.md) for overview
- Check [RENDER_SETUP.md](RENDER_SETUP.md) for deployment help
- Ask questions in GitHub Discussions

## Code Style Guidelines

- Follow PEP 8 (enforced by Black and Ruff)
- Use type hints for all function signatures
- Write docstrings for all public functions and classes
- Keep functions focused and single-purpose
- Write tests for new features
- Maintain test coverage above 80%

## Commit Message Convention

```
type(scope): subject

body (optional)

footer (optional)
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:
```
feat(auth): add OAuth Google login

Implements Google OAuth2 authentication flow with JWT tokens.

Closes #123
```

## Pull Request Process

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make your changes with clear commits
3. Add/update tests as needed
4. Run quality checks: `black . && ruff check . && pytest`
5. Push and create a Pull Request
6. Ensure CI passes
7. Request review from maintainers

Thank you for contributing to Umatter! 🎉
