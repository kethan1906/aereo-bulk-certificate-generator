# ⚡ AEREO | Bulk Certificate Generator API

<p align="center">
  <strong>Generate. Track. Download.</strong>
  <br />
  A backend API for generating and managing PDF certificates in bulk.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-REST%20API-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Testing-Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" alt="Pytest" />
  <img src="https://img.shields.io/badge/Output-PDF-DC2626?style=for-the-badge" alt="PDF generation" />
</p>

---

## 📌 Overview

The **AEREO Bulk Certificate Generator API** is a backend project designed to simplify the creation and retrieval of PDF certificates for multiple recipients.

Instead of generating certificates individually, clients can submit a batch of recipient details through a REST API. The application processes the request, tracks the generation job, and provides access to the resulting certificates.

Built with **Python and FastAPI**, the project demonstrates API development, request validation, job management, PDF generation, error handling, and automated testing.

## ✨ Key Features

* **📦 Bulk Processing** — Submit multiple recipients in a single generation request.
* **📄 PDF Certificates** — Generate downloadable certificate documents.
* **🔄 Job Tracking** — Monitor generation jobs and their processing status.
* **✅ Input Validation** — Validate incoming request data and handle invalid inputs.
* **⬇️ Certificate Downloads** — Retrieve generated certificates through API endpoints.
* **🛡️ Error Handling** — Return appropriate API responses for invalid requests and unsuccessful operations.
* **🧪 Automated Testing** — Test API behavior and important application workflows with pytest.
* **📚 Interactive Documentation** — Explore and execute API requests using Swagger UI.

## 🏗️ Architecture

```text
           Client / API Consumer
                    |
                    v
             FastAPI REST API
                    |
                    v
          Request Validation
                    |
                    v
          Generation Job Manager
                    |
                    v
           PDF Certificate Engine
                    |
                    v
           Generated Certificates
                    |
                    v
             Download Endpoint
```

**Workflow:** A client submits recipient data → the API validates the request → a generation job is created → certificates are generated → the client checks job status and downloads the resulting PDFs.

## 🛠️ Tech Stack

| Technology             | Purpose                        |
| ---------------------- | ------------------------------ |
| Python                 | Core programming language      |
| FastAPI                | REST API framework             |
| Uvicorn                | ASGI application server        |
| Pydantic               | Request data validation        |
| Pytest                 | Automated testing              |
| PDF generation library | Creating certificate documents |

*The exact PDF library and other dependencies are defined in `requirements.txt`.*

## 📂 Project Structure

```text
aereo-bulk-certificate-generator/
│
├── app/             # API routes and application logic
├── tests/           # Automated tests
├── generated/       # Generated certificate output
├── .gitignore       # Files excluded from version control
├── README.md        # Project documentation
├── requirements.txt # Python dependencies
└── .venv/           # Local virtual environment (not committed)
```

*The displayed structure is illustrative; filenames may vary depending on the repository.*

## 🚀 Getting Started

### Prerequisites

* Python 3.10 or newer
* pip
* Git (optional, for cloning the repository)

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/aereo-bulk-certificate-generator.git
cd aereo-bulk-certificate-generator
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create a virtual environment

**Windows PowerShell**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
py -m pip install -r requirements.txt
```

### 4. Run the application

```powershell
py -m uvicorn app.main:app --reload
```

The API server will be available at:

* **Swagger UI:** http://127.0.0.1:8000/docs
* **OpenAPI schema:** http://127.0.0.1:8000/openapi.json

Keep the terminal running while using the API.

## 🧪 Run Tests

Execute the automated test suite from the project root:

```powershell
py -m pytest -q
```

The command runs the available tests and reports the number of passed and failed cases.

## 🔌 API Usage

Explore the available endpoints in Swagger UI at `http://127.0.0.1:8000/docs`.

The primary workflow includes:

1. **Create a generation job** — Submit event information and recipient details.
2. **Track job progress** — Retrieve the job status using its job ID.
3. **Review generation results** — Check successful and failed recipient counts.
4. **Download certificates** — Retrieve the generated PDF using its certificate ID.

Endpoint paths and request schemas can be verified in the interactive API documentation.

## 🔒 Security & Best Practices

* Keep environment variables and credentials out of version control.
* Exclude virtual environments, test caches, and unnecessary generated files.
* Validate incoming request data.
* Avoid committing real recipient information or confidential certificates.
* Use appropriate access controls before deploying the API publicly.

## 🎯 What This Project Demonstrates

* Designing RESTful APIs with FastAPI.
* Handling structured JSON requests and validation.
* Building a bulk-processing workflow.
* Generating and serving PDF files.
* Tracking job status and processing results.
* Writing automated tests with pytest.
* Documenting and testing APIs through Swagger UI.

## 🔮 Future Improvements

* Add background task processing for larger batches.
* Introduce persistent storage for job metadata.
* Add authentication and role-based access control.
* Support customizable certificate templates.
* Add deployment automation and continuous integration.

## 👨‍💻 Author
M.Srinikethan


Python | Backend Development | REST APIs

[GitHub Profile](https://github.com/kethan1906)

---

<p align="center">
  <strong>Built with Python. Designed for scalable certificate workflows. ⚡</strong>
</p>
