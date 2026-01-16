from pydantic import BaseModel, Field, model_validator
from typing import List, Literal


class MDPRelativeValueIterationRequest(BaseModel):
    TPM: List[List[List[float]]]
    TRM: List[List[List[float]]]
    s_ref: int = Field(..., description="Reference state index (0 ≤ s_ref < n)")
    epsilon: float = Field(..., gt=1e-12, description="Convergence tolerance (must be > 1e-12)")
    mode: Literal["cost", "reward"] = "cost"

    @model_validator(mode="after")
    def validate_dimensions_and_indices(self):
        tpm = self.TPM
        trm = self.TRM

        # --- Basic structural validation ---
        if len(tpm) == 0:
            raise ValueError("TPM must have at least one state")

        n = len(tpm)

        # Validate s_ref bounds
        if not (0 <= self.s_ref < n):
            raise ValueError(f"s_ref must be between 0 and {n-1}, got {self.s_ref}")

        # Validate TPM and TRM shapes (n, n, A)
        for name, tensor in [("TPM", tpm), ("TRM", trm)]:
            if len(tensor) != n:
                raise ValueError(f"{name} must have shape (n, n, A) with n={n}")

            for row in tensor:
                if len(row) != n:
                    raise ValueError(f"{name} must have shape (n, n, A) with n={n}")

        # Determine number of actions A
        A = len(tpm[0][0])

        # Validate consistent action dimension across TPM
        for i in range(n):
            for j in range(n):
                if len(tpm[i][j]) != A:
                    raise ValueError(
                        f"TPM has inconsistent action dimension at (i={i}, j={j}). "
                        f"Expected A={A}, got {len(tpm[i][j])}"
                    )

        # Validate TRM matches TPM action dimension
        for i in range(n):
            for j in range(n):
                if len(trm[i][j]) != A:
                    raise ValueError(
                        f"TRM must have the same action dimension A={A} as TPM. "
                        f"Mismatch at (i={i}, j={j})"
                    )

        # --- Validate TPM stochasticity and non-negativity ---
        for i in range(n):
            for a in range(A):
                row = [tpm[i][j][a] for j in range(n)]

                # Non-negativity
                if any(p < 0 for p in row):
                    raise ValueError(
                        f"TPM contains negative probability at state {i}, action {a}. "
                        f"Row: {row}"
                    )

                # Row must sum to 1
                row_sum = sum(row)
                if abs(row_sum - 1.0) > 1e-8:
                    raise ValueError(
                        f"TPM row for state {i}, action {a} must sum to 1. Got {row_sum}"
                    )

        return self


class MDPRelativeValueIterationResponse(BaseModel):
    h: List[float]
    g: float
    pi_star: List[int]
    iterations: int
    converged: bool
