# Flask User Management App — CI/CD Pipeline with Unit & Selenium Testing

A containerised Flask + MySQL web application with a five-stage Jenkins CI/CD pipeline covering linting, Docker builds, unit tests, deployment, and end-to-end Selenium browser tests.

---

## Architecture Overview

```
GitHub (push trigger)
        │
        ▼
  Jenkins Pipeline
        │
        ├── 1. Code Linting         → pylint on app.py (venv)
        ├── 2. Code Build           → Docker image build & tag
        ├── 3. Unit Testing         → pytest (test_app.py)
        ├── 4. Containerised Deploy → docker-compose up (app + MySQL)
        └── 5. Selenium Testing     → headless Chrome in Docker container
```

**Stack:**
- **Backend:** Python / Flask
- **Database:** MySQL 8.0
- **Containerisation:** Docker + Docker Compose
- **CI/CD:** Jenkins
- **Unit Tests:** pytest
- **E2E Tests:** Selenium (headless Chrome)
- **Linting:** pylint

---

## Project Structure

```
.
├── app.py                   # Flask application (users CRUD + health check)
├── templates/
│   └── index.html           # User Management UI
├── requirements.txt         # Python dependencies
├── Dockerfile               # App container image
├── Dockerfile.selenium      # Selenium test runner image (Chrome + ChromeDriver)
├── docker-compose.yml       # Orchestrates app + MySQL services
├── init.sql                 # DB schema and seed data
└── tests/
    ├── test_app.py          # Unit tests (pytest)
    └── selenium_tests.py    # End-to-end browser tests (Selenium)
```

---

## Application

A simple User Management System with three routes:

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Displays all users from the database |
| `/add` | POST | Inserts a new user (name + email) |
| `/health` | GET | Health check — returns `{"status": "healthy"}` |

Database connection is configured via environment variables:

| Variable | Default |
|----------|---------|
| `DB_HOST` | `localhost` |
| `DB_USER` | `root` |
| `DB_PASSWORD` | `password` |
| `DB_NAME` | `myapp` |

The `users` table is initialised automatically on first run via `init.sql`, which also seeds two example records.

---

## Docker Compose

Two services run on a shared `myapp-network` bridge network:

| Service | Image | Port | Notes |
|---------|-------|------|-------|
| `db` | `mysql:8.0` | — (internal) | Health-checked; app waits for it to be ready |
| `app` | built from `Dockerfile` | `5000:5000` | Starts only after `db` passes health check |

```bash
# Start the full stack
docker-compose up -d

# Tear down
docker-compose down
```

---

## CI/CD Pipeline (Jenkinsfile)

### Stage 1 — Code Linting
Creates a Python virtual environment, installs pylint, and runs it against `app.py`. Conventions and bare-except warnings are suppressed; the stage is non-blocking (failures don't stop the pipeline).

### Stage 2 — Code Build
Builds the Docker image tagged with the Jenkins build number and also tags it as `latest`.

### Stage 3 — Unit Testing
Activates the venv, installs dependencies, and runs `tests/test_app.py` with pytest. Tests covered:

- `test_health_endpoint` — asserts `/health` returns 200 and `{"status": "healthy"}`
- `test_index_page` — asserts `/` returns 200 and contains the page heading

### Stage 4 — Containerised Deployment
Stops and removes all running containers, then brings the full stack up with `docker-compose up -d`. Waits 20 seconds for services to stabilise before logging output.

### Stage 5 — Selenium Testing
Builds a dedicated test image (`Dockerfile.selenium`) containing Google Chrome and ChromeDriver, then runs it inside the Compose network so it can reach `http://app:5000`. Tests covered:

- `test_page_title` — waits for the `<h1>` tag and confirms "User Management" is present
- `test_add_user_form` — locates the name field, email field, and submit button by ID and asserts they are visible and functional

**Post-pipeline:** Compose logs are always printed. On failure, `docker-compose down` is called automatically.

---

## Running Locally

### With Docker Compose
```bash
docker-compose up -d
# App available at http://localhost:5000
```

### Unit Tests Only
```bash
python3 -m venv venv && . venv/bin/activate
pip install -r requirements.txt
pytest tests/test_app.py -v
```

### Selenium Tests (requires running stack)
```bash
# Build the Selenium image
docker build -f Dockerfile.selenium -t selenium-tests .

# Run against the Compose network
docker run --rm \
    --network my-web-app_default \
    selenium-tests
```

---

## Dependencies

```
Flask==2.3.0
Werkzeug==2.3.7
mysql-connector-python==8.0.33
pytest==7.3.1
selenium==4.9.0
pylint==2.17.4
```
