from fastapi import FastAPI
from logging import getLogger
import numpy as np

from app.models import(
    MDPRelativeValueIterationRequest,
    MDPRelativeValueIterationResponse
)
from app.markov_decisions import (
    relative_value_iteration_average_reward
)

from app.logging_config import setup_logging

setup_logging()
logger = getLogger(__name__)


app = FastAPI(
    title="Markov Decision Service",
    description="A microservice providing Markov Decision Process solutions.",
    version="0.1.0",
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post( "/mdp/relative-value-iteration", response_model=MDPRelativeValueIterationResponse )
def solve_mdp_average_reward_RVI(request: MDPRelativeValueIterationRequest):
    TPM = np.array(request.TPM)
    TRM = np.array(request.TRM)

    logger.info(f"TPM shape: {TPM.shape}, TRM shape: {TRM.shape}")

    # Normalize reward vs cost semantics 
    if request.mode == "reward": TRM = -TRM

    h, g, pi_star, last_iteration, converged = relative_value_iteration_average_reward(
        TPM, TRM, request.s_ref, request.epsilon
    )

    return {
        "h": h.tolist(),
        "g": g,
        "pi_star": pi_star.tolist(),
        "iterations":last_iteration ,
        "converged": converged
    }
