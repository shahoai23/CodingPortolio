# Reliability Service — Architecture Overview

This microservice provides reliability calculations commonly used in aerospace and reliability engineering. It exposes a FastAPI-based HTTP interface and includes structured logging and Prometheus metrics.

## High-Level Architecture

- **API Layer (FastAPI)**  
  Handles routing, request validation, and responses.

- **Domain Logic (`reliability.py`)**  
  Contains reliability math functions (exponential reliability, MTBF conversions, series systems).

- **Data Models (Pydantic)**  
  Defines request/response schemas for API endpoints.

- **Observability**
  - Structured logging
  - `/metrics` endpoint (Prometheus format)
  - `/health` and `/ready` endpoints

- **Containerization**
  - Dockerfile for reproducible deployment