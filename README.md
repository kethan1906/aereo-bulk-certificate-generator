# AEREO Bulk Certificate Generator API

A REST API built with FastAPI to generate and manage certificates in bulk. The application accepts recipient information, creates a generation job, generates PDF certificates, and provides endpoints to track job status and retrieve certificates.

## Features

* Bulk certificate generation through a single API request.
* REST endpoints for creating jobs, checking job status, and retrieving certificates.
* PDF certificate generation using ReportLab.
* Request validation using Pydantic.
* Database operations using SQLAlchemy and SQLite by default.
* Job tracking and error handling.
* Isolation of individual certificate-generation failures.
* Interactive API documentation through Swagger UI.
* Automated tests using Pytest.

## Technology Stack

| Technology | Purpose                         |
| ---------- | ------------------------------- |
| Python     | Main programming language       |
| FastAPI    | REST API framework              |
| Uvicorn    | Application server              |
| Pydantic   | Request and response validation |
| SQLAlchemy | Database operations             |
| SQLite     | Default database                |
| ReportLab  | PDF generation                  |
| Pytest     | Automated testing               |

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

The `generated/` directory contains runtime output when configured by the application. Generated files should generally not be committed to the repository.

## Prerequisites

* Python installed on your system.
* Git, if you want to clone the repository and work locally.

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

### 3. Activate the environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

### 4. Install dependencies

```powershell
py -m pip install -r requirements.txt
```

### 5. Start the API

```powershell
py -m uvicorn app.main:app --reload
```

The application should be available at:

`http://127.0.0.1:8000`

### 6. Open the API documentation

Visit:

`http://127.0.0.1:8000/docs`

Use Swagger UI to inspect the available endpoints and test requests.

### 7. Run the tests

```powershell
py -m pytest -q
```

Review the terminal output to confirm whether the tests pass.

## API Endpoints

| Method | Endpoint                                | Description                          |
| ------ | --------------------------------------- | ------------------------------------ |
| `POST` | `/api/v1/generation-jobs`               | Creates a certificate generation job |
| `GET`  | `/api/v1/generation-jobs/{job_id}`      | Retrieves job status and results     |
| `GET`  | `/api/v1/certificates/{certificate_id}` | Retrieves a generated certificate    |
| `GET`  | `/health`                               | Checks application health            |

### Create a generation job

`POST /api/v1/generation-jobs`

Submit recipient information in the JSON format expected by the request schema. The application validates the request and creates a generation job.

### Check generation status

`GET /api/v1/generation-jobs/{job_id}`

Use the job ID returned by the API to check the job's status and available results.

### Retrieve a certificate

`GET /api/v1/certificates/{certificate_id}`

Use a valid certificate ID to retrieve the corresponding certificate.

### Health check

`GET /health`

Checks the application's health endpoint.

## How It Works

1. The client submits recipient information through the API.
2. FastAPI validates the request using Pydantic.
3. The application creates a generation job and records relevant information in the database.
4. The generation workflow creates PDF certificates using ReportLab.
5. Job status and certificate information are made available through the API.
6. The client can check job status and retrieve certificates using their IDs.

The application uses FastAPI background tasks for job processing. For large-scale production workloads, a dedicated task queue could provide more durable processing and retry capabilities.

## Error Handling and Validation

The application validates incoming requests and handles errors that occur during certificate generation. Individual recipient failures can be isolated so that one failed certificate does not necessarily stop processing the remaining recipients.

## Future Improvements

* Add a dedicated task queue for durable background processing.
* Add database migrations using Alembic.
* Implement authentication and authorization.
* Support additional certificate templates and custom fonts.
* Improve logging, monitoring, and retry mechanisms.
* Add continuous integration to run tests automatically.
* Prepare deployment configuration for production.

## Author

**M. Srinikethan**

GitHub: [kethan1906](https://github.com/kethan1906)

## License

A license has not yet been specified. Add a license file if you intend to distribute this project under a particular open-source license.
