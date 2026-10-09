# AEREO Bulk Certificate Generator API

A REST API built using **FastAPI** to generate and manage certificates in bulk. The application accepts recipient details, creates a generation job, generates certificates in PDF format, and provides endpoints to track job status and retrieve generated certificates.

## Features

* **Bulk certificate generation:** Generate certificates for multiple recipients through a single API request.
* **REST API:** Exposes endpoints to create generation jobs, check job status, and retrieve certificates.
* **PDF generation:** Uses ReportLab to create certificate PDFs.
* **Job tracking:** Tracks the status and results of certificate generation jobs.
* **Database integration:** Uses SQLAlchemy with SQLite as the default database.
* **Input validation:** Uses Pydantic schemas to validate API requests.
* **Error handling:** Handles invalid requests and generation failures.
* **Failure isolation:** A failure while generating one recipient's certificate does not necessarily prevent processing the remaining recipients.
* **API documentation:** Provides interactive API documentation through FastAPI's Swagger UI.
* **Automated tests:** Includes tests for API endpoints, validation, certificate generation, and failure scenarios.

## Tech Stack

| Technology | Purpose                                            |
| ---------- | -------------------------------------------------- |
| Python     | Main programming language                          |
| FastAPI    | Builds the REST API                                |
| Uvicorn    | Runs the application server                        |
| Pydantic   | Validates request and response data                |
| SQLAlchemy | Handles database operations                        |
| SQLite     | Stores job and certificate-related data by default |
| ReportLab  | Generates PDF certificates                         |
| Pytest     | Tests application functionality                    |

## Project Architecture

The application follows a modular structure, separating API endpoints, business logic, database operations, data models, and utility functions.

```text
aereo-bulk-certificate-generator/
│
├── app/
│   ├── api/             # API routes and endpoints
│   ├── core/            # Application configuration
│   ├── db/              # Database setup and session management
│   ├── models/          # Database models
│   ├── repositories/    # Database access operations
│   ├── schemas/         # Request and response validation
│   ├── services/        # Certificate generation and job logic
│   ├── templates/       # Certificate templates
│   ├── utils/           # Shared utility functions
│   └── main.py          # FastAPI application entry point
│
├── tests/               # Automated tests
├── generated/           # Generated output, if configured locally
├── requirements.txt     # Python dependencies
├── .gitignore           # Files excluded from Git
└── README.md            # Project documentation
```

*Note: This is a high-level overview. Ensure the directory names match the actual folders in the repository.*

## Prerequisites

Install the following before running the project:

* Python 3.10 or a compatible version supported by the dependencies
* Git
* A terminal such as PowerShell or Command Prompt

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/kethan1906/aereo-bulk-certificate-generator.git
cd aereo-bulk-certificate-generator
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
py -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, you can use Command Prompt instead:

```cmd
.venv\Scripts\activate.bat
```

### 4. Install dependencies

```powershell
py -m pip install -r requirements.txt
```

### 5. Start the application

```powershell
py -m uvicorn app.main:app --reload
```

The API should now be available at:

`http://127.0.0.1:8000`

### 6. Open the API documentation

Visit:

`http://127.0.0.1:8000/docs`

Use the interactive Swagger UI to inspect the endpoints, provide request data, and test the API.

### 7. Run the tests

Open another terminal in the project directory, activate the virtual environment, and run:

```powershell
py -m pytest -q
```

The command runs the automated test suite. Confirm the results in your terminal before reporting the test count.

## API Endpoints

The API exposes the following endpoints:

| Method | Endpoint                                | Description                                          |
| ------ | --------------------------------------- | ---------------------------------------------------- |
| `POST` | `/api/v1/generation-jobs`               | Creates a certificate generation job                 |
| `GET`  | `/api/v1/generation-jobs/{job_id}`      | Retrieves the status and results of a generation job |
| `GET`  | `/api/v1/certificates/{certificate_id}` | Retrieves a generated certificate                    |
| `GET`  | `/health`                               | Checks application health                            |

### 1. Create a generation job

**Endpoint:**

```http
POST /api/v1/generation-jobs
```

Submit the recipient information and any other fields required by the request schema. The API validates the input and creates a generation job.

Check the request schema in `/docs` for the exact JSON format expected by the application.

### 2. Check job status

**Endpoint:**

```http
GET /api/v1/generation-jobs/{job_id}
```

Replace `{job_id}` with the ID returned when the generation job was created. The response provides the available job status and result information.

### 3. Retrieve a certificate

**Endpoint:**

```http
GET /api/v1/certificates/{certificate_id}
```

Replace `{certificate_id}` with a valid certificate ID. The endpoint retrieves the corresponding certificate according to the application's response implementation.

### 4. Check application health

**Endpoint:**

```http
GET /health
```

Returns the application's health-check response.

## How It Works

1. A client submits recipient details through the certificate generation endpoint.
2. FastAPI validates the request using Pydantic schemas.
3. The application creates a generation job and records the relevant information in the database.
4. The generation workflow processes the recipients and creates PDF certificates using ReportLab.
5. Job status and certificate details are made available through the API.
6. Clients can check the job status and retrieve generated certificates using their IDs.

The implementation uses FastAPI background tasks for asynchronous job processing within the application. These tasks are not a replacement for a dedicated, durable task queue in a large-scale production system.

## Error Handling and Validation

The application is designed to handle invalid inputs and certificate-generation errors. Request validation helps prevent malformed data from reaching the business logic. Failure isolation allows the application to handle individual recipient failures without unnecessarily stopping the entire batch.

The exact HTTP status codes and error response formats depend on the implemented endpoint behavior.

## Configuration and Generated Files

SQLite is the default database configuration. Review the application configuration before changing database settings.

Generated certificates and other runtime files should generally remain outside version control unless the assignment explicitly requires sample outputs to be committed.

## Future Improvements

Possible improvements include:

* Integrating a dedicated task queue, such as Celery or RQ, for durable background processing.
* Adding database migrations with Alembic.
* Implementing authentication and role-based authorization.
* Supporting additional certificate templates and custom fonts.
* Improving logging, monitoring, and retry mechanisms.
* Adding continuous integration to run automated tests on each pull request.
* Adding deployment configuration for a production environment.

## Author

**M. Srinikethan**

GitHub: [kethan1906](https://github.com/kethan1906)


