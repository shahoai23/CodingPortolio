# Component Diagram
+---------------------------------------------------------------+
|                     Reliability Service                       |
|---------------------------------------------------------------|
|                                                               |
|   +----------------+       +----------------+                 |
|   |   API Layer    |       |  Domain Logic  |                 |
|   | (FastAPI)      |       | (reliability.py)|                |
|   +----------------+       +----------------+                 |
|   | - main.py      |       | - math funcs   |                 |
|   | - routes       |       | - reliability  |                 |
|   | - middleware   |       |   calculations |                 |
|   +----------------+       +----------------+                 |
|                                                               |
|   +----------------+       +----------------+                 |
|   | Data Models    |       | Observability  |                 |
|   | (Pydantic)     |       | (logging,      |                 |
|   +----------------+       |  metrics)       |                 |
|   | - Request DTOs |       +----------------+                 |
|   | - Response DTOs|       | - logging_config|                |
|   +----------------+       | - /metrics      |                |
|                                                               |
+---------------------------------------------------------------+