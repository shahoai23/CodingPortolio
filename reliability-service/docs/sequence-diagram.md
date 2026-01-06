
---

# 📄 `sequence-diagram.md`  
**Purpose:** Show how a request flows through the system.

```markdown
# Sequence Diagram — Exponential Reliability Request
Client -> FastAPI: POST /reliability/exponential
FastAPI -> Pydantic: Validate request payload
Pydantic --> FastAPI: Validated model
FastAPI -> reliability.py: exponential_reliability(λ, t)
reliability.py --> FastAPI: reliability value
FastAPI -> Prometheus: Update counters/histograms
FastAPI --> Client: JSON response { "reliability": R }