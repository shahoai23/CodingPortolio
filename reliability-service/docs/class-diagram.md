
---

# class-diagram.md
**Purpose:** Show internal structure — classes, functions, relationships.

```markdown
# Class Diagram
+---------------------------+
|      FastAPI App         |
+---------------------------+
| + health()               |
| + ready()                |
| + metrics()              |
| + compute_exponential()  |
| + compute_mtbf()         |
| + compute_series()       |
+---------------------------+
            |
            v
+---------------------------+
|   Pydantic Models         |
+---------------------------+
| ExponentialReliabilityRequest |
| ExponentialReliabilityResponse|
| MtbfRequest                    |
| MtbfResponse                   |
| SeriesSystemRequest            |
| SystemReliabilityResponse      |
+---------------------------+
            |
            v
+---------------------------+
|   reliability.py          |
+---------------------------+
| + exponential_reliability() |
| + mtbf_to_failure_rate()    |
| + series_system_reliability()|
+---------------------------+