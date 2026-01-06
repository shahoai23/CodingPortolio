from fastapi import FastAPI
from logging import getLogger

from app.models import (
    ExponentialReliabilityRequest,
    ExponentialReliabilityResponse,
    MtbfConversionRequest,
    MtbfConversionResponse,
    SeriesSystemRequest,
    SeriesSystemResponse,
    KofNSystemRequest,
    KofNSystemResponse,
)

from app.reliability import (
    exponential_reliability,
    mtbf_failure_rate_convert,
    series_system_reliability,
    kofn_system_reliability,
)

from app.logging_config import setup_logging


# -----------------------------
# App Initialization
# -----------------------------

setup_logging()
logger = getLogger(__name__)

app = FastAPI(
    title="Reliability Service",
    description="A microservice providing reliability engineering calculations.",
    version="0.1.0",
)


# -----------------------------
# Health Check
# -----------------------------

@app.get("/health")
def health_check():
    return {"status": "ok"}


# -----------------------------
# Reliability Endpoints
# -----------------------------

@app.post("/reliability/exponential", response_model=ExponentialReliabilityResponse)
def compute_exponential(req: ExponentialReliabilityRequest):
    logger.info("Computing exponential reliability")
    result = exponential_reliability(req.failure_rate, req.mission_time)
    return ExponentialReliabilityResponse(reliability=result)


@app.post("/reliability/mtbf-convert", response_model=MtbfConversionResponse)
def convert_mtbf(req: MtbfConversionRequest):
    logger.info("Converting MTBF/failure rate")
    result = mtbf_failure_rate_convert(req.value)
    return MtbfConversionResponse(converted_value=result)


@app.post("/reliability/series", response_model=SeriesSystemResponse)
def compute_series(req: SeriesSystemRequest):
    logger.info("Computing series system reliability")
    result = series_system_reliability(req.component_reliabilities)
    return SeriesSystemResponse(reliability=result)


@app.post("/reliability/kofn", response_model=KofNSystemResponse)
def compute_kofn(req: KofNSystemRequest):
    logger.info("Computing k-of-n system reliability")
    result = kofn_system_reliability(req.component_reliabilities, req.min_required)
    return KofNSystemResponse(reliability=result)