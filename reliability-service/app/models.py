from pydantic import BaseModel, Field
from typing import List, TypeAlias, Annotated

# Constrained float: > 0 and ≤ 1
ReliabilityValue = Annotated[float, Field(gt=0, le=1)]

# Constrained list: at least 1 item, each item must be a ReliabilityValue
ReliabilityList = Annotated[list[ReliabilityValue], Field(min_length=1)]


# -----------------------------
# Exponential Reliability Models
# -----------------------------

class ExponentialReliabilityRequest(BaseModel):
    failure_rate: float = Field(
        ge=0,
        description="Failure rate λ (must be > 0)"
    )
    mission_time: float = Field(
        ge=0,
        description="Mission time t (must be ≥ 0)"
    )


class ExponentialReliabilityResponse(BaseModel):
    reliability: float


# -----------------------------
# MTBF / Failure Rate Conversion
# -----------------------------

class MtbfConversionRequest(BaseModel):
    value: float = Field(
        gt=0,
        description="MTBF or failure rate (must be > 0)"
    )


class MtbfConversionResponse(BaseModel):
    converted_value: float


# -----------------------------
# Series System Reliability
# -----------------------------

class SeriesSystemRequest(BaseModel):
    component_reliabilities: ReliabilityList = Field( description="List of component reliabilities (each > 0 and ≤ 1)")



class SeriesSystemResponse(BaseModel):
    reliability: float


# -----------------------------
# k-of-n System Reliability
# -----------------------------

class KofNSystemRequest(BaseModel):
    component_reliabilities: ReliabilityList = Field( description="List of component reliabilities (each > 0 and ≤ 1)")
    
    min_required: int = Field(
        gt=0,
        description="Minimum number of components required for system success"
    )


class KofNSystemResponse(BaseModel):
    reliability: float