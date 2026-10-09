# AEREO Bulk Certificate Generator API

A REST API built with **FastAPI** to generate, manage, and retrieve PDF certificates in bulk. The application accepts recipient information, creates generation jobs, tracks processing status, and provides endpoints to retrieve generated certificates.

## Features

* Bulk certificate generation through a single API request.
* RESTful API endpoints for job creation, status tracking, and certificate retrieval.
* PDF certificate generation using ReportLab.
* Request validation using Pydantic.
* Database operations using SQLAlchemy and SQLite.
* Background processing using FastAPI Background Tasks.
* Error handling and isolation of individual certificate-generation failures.
* Interactive API documentation through Swagger UI.
* Automated testing using Pytest.
* Health-check endpoint to verify application availability.

## Technology Stack

| Technology | Purpose                         |
| ---------- | ------------------------------- |
| Python     | Core programming language       |
| FastAPI    | REST API development            |
| Uvicorn    | ASGI application server         |
| Pydantic   | Request and response validation |
| SQLAlchemy | Database operations and ORM     |
| SQLite     | Default database                |
| ReportLab  | PDF certificate generation      |
| Pytest     | Automated testing               |
| Swagger UI | Interactive API documentation   |

## System Architecture

The application follows a layered architecture that separates API handling, validation, business logic, database operations, and PDF generation.

```text
              Client / API Consumer
                       |
                       v
                FastAPI Application
                       |
                       v
                Pydantic Validation
                       |
                       v
                  API Routes
                       |
                       v
                  Service Layer
                       |
             +---------+---------+
             |                   |
             v                   v
       Data Access Layer    PDF Generation
             |                   |
             v                   v
         SQLAlchemy            ReportLab
             |                   |
             v                   v
           SQLite         Generated PDF Files
             |                   |
             +---------+---------+
                       |
                       v
              Job Status and Results
                       |
                       v
                Client Retrieval
```

### Architecture Components

* **API Layer:** Exposes REST endpoints and handles incoming HTTP requests.
* **Validation Layer:** Uses Pydantic to validate request data and enforce schema requirements.
* **Service Layer:** Coordinates generation jobs, certificate creation, and error handling.
* **Data Access Layer:** Uses SQLAlchemy to interact with the database.
* **Database:** SQLite stores job and certificate-related information.
* **PDF Generation:** ReportLab creates PDF certificates.
* **Background Processing:** FastAPI Background Tasks supports processing after the initial response.
* **Testing Layer:** Pytest verifies application behavior and API functionality.

## Project Structure

```text
aereo-bulk-certificate-generator/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   ├── deps.py
│   │   └── router.py
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   ├── templates/
│   ├── utils/
│   └── main.py
├── tests/
├── generated/
├── requirements.txt
├── .gitignore
└── README.md
```

The `generated/` directory stores runtime-generated files when configured by the application. Generated PDFs and other temporary artifacts should generally not be committed to Git.

## Prerequisites

Before running the project, ensure you have:

* Python 3.10 or a compatible version supported by the project's dependencies.
* Git, if cloning the repository.
* A terminal or command prompt.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/kethan1906/aereo-bulk-certificate-generator.git
cd aereo-bulk-certificate-generator
```

### 2. Create a Virtual Environment

On Windows:

```powershell
py -m venv .venv
```

### 3. Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

For Windows Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

### 4. Install Dependencies

```powershell
py -m pip install -r requirements.txt
```

### 5. Start the Application

```powershell
py -m uvicorn app.main:app --reload
```

The API should now be available at:

http://127.0.0.1:8000

### 6. Access API Documentation

Open the following URL in your browser:

http://127.0.0.1:8000/docs

Swagger UI allows you to inspect available endpoints, submit requests, and view API responses.

Alternative API documentation is available at:

http://127.0.0.1:8000/redoc

## API Endpoints

| Method | Endpoint                                | Description                          |
| ------ | --------------------------------------- | ------------------------------------ |
| `POST` | `/api/v1/generation-jobs`               | Creates a certificate generation job |
| `GET`  | `/api/v1/generation-jobs/{job_id}`      | Retrieves job status and results     |
| `GET`  | `/api/v1/certificates/{certificate_id}` | Retrieves a generated certificate    |
| `GET`  | `/health`                               | Checks application health            |

### 1. Create a Generation Job

**Endpoint:** `POST /api/v1/generation-jobs`

Accepts recipient information and initiates a certificate generation job.

The request body must follow the schema defined by the application. The API validates the input and returns information about the created job.

### 2. Check Job Status

**Endpoint:** `GET /api/v1/generation-jobs/{job_id}`

Retrieves the status and available results of a generation job.

Use the `job_id` returned when creating the job.

### 3. Retrieve a Certificate

**Endpoint:** `GET /api/v1/certificates/{certificate_id}`

Retrieves the certificate associated with the supplied certificate ID, according to the endpoint's response implementation.

### 4. Health Check

**Endpoint:** `GET /health`

Checks whether the application's health endpoint is responding.

## How the Application Works

1. **Request Submission:** The client submits recipient information through the REST API.
2. **Input Validation:** FastAPI and Pydantic validate the incoming request.
3. **Job Creation:** The application creates a generation job and stores relevant information in the database.
4. **Certificate Generation:** The processing workflow uses ReportLab to generate PDF certificates.
5. **Error Handling:** Individual generation failures can be handled without necessarily stopping the entire batch.
6. **Status Tracking:** The client checks the job status using the job ID.
7. **Certificate Retrieval:** The client retrieves available certificates using their certificate IDs.

## Error Handling and Validation

The application is designed to validate incoming data and handle errors during certificate generation.

Key considerations include:

* Rejecting invalid request data.
* Handling missing or invalid job and certificate IDs.
* Recording job status and certificate-generation results.
* Isolating individual certificate failures where supported by the implementation.
* Returning appropriate HTTP responses for API errors.

## Running Automated Tests

Run the test suite from the project root:

```powershell
py -m pytest -q
```

Pytest executes the available automated tests and displays a summary of passed and failed tests.

For more detailed output:

```powershell
py -m pytest -v
```

## Future Improvements

* Introduce Celery or another dedicated task queue for durable background processing.
* Add database migrations using Alembic.
* Implement authentication and authorization.
* Add configurable certificate templates, branding, and custom fonts.
* Improve logging, monitoring, and retry mechanisms.
* Add continuous integration to run tests automatically.
* Introduce deployment configuration for production environments.
* Add batch-level progress reporting and downloadable certificate archives.
* Add rate limiting and stronger request-size validation.

## License

Add a license file if you intend to distribute the project publicly. Until a license is specified, the repository's reuse terms should not be assumed.

## Author

**M. Srinikethan**

GitHub: [kethan1906](https://github.com/kethan1906)
