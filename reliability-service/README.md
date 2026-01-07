# Reliability Service API

A containerized FastAPI microservice that provides core reliability engineering calculations, including exponential reliability, MTBF conversions, series system reliability, and k‑of‑n redundancy modeling. This project blends classical reliability engineering with modern software engineering practices, cloud readiness, and clean API design.

---

## Features

### Reliability Calculations
- **Exponential reliability** — computes \( R(t) = e^{-\lambda t} \)
- **MTBF conversions** — converts between MTBF and failure rate for exponential distributions
- **Series system reliability** — multiplies component reliabilities for series configurations
- **k‑of‑n redundancy** — computes system reliability when any *k* of *n* components must succeed

### Modern Software Engineering
- FastAPI backend with automatic OpenAPI/Swagger documentation
- Pydantic v2 models for strict validation and type safety
- Clean, modular project layout for maintainability
- Fully containerized using Docker for consistent deployment

### Testing
- Pytest-based test suite
- Endpoint-level API tests using `httpx`
- Clear separation between domain logic and API routing

---

## Project Structure
reliability-service/
│
├── app/
│   ├── main.py           # FastAPI application and routing
│   ├── models.py         # Pydantic request/response models
│   ├── reliability.py    # Core reliability math functions
│   └── init.py
│
├── tests/
│   └── test_reliability.py
│
├── Dockerfile
├── .dockerignore
├── requirements.txt
└── README.md

## Build instructions
docker build -t reliability-service .
docker run -p 8000:8000 reliability-service


### Access the API
Interactive documentation is available at:
http://localhost:8000/docs

## Future Work
--Availability Calculcations
--Dissimilar k of n calculcations
--deployment to cloud
--cloud monitoring
-SLOs, SLIs, and error budget tracking
-- UI