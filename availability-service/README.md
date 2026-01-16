# Availability Service API

A containerized FastAPI microservice that provides core availability calculcations when provided reliability and maintainability data.

---
## Intended Features

1. Basic Ai calculcations when provided Meant time between downing event and mean time of downing event
2. Availability calculations using markov model analysis for CTMC or DTMC (textbook reliability engineering approaches)
3. Availability calculation using MDP style cost calculation (weighted graph traversal)
4. Service Availability calculation for a semi markov case (delayed maintenance action for non critical failure)