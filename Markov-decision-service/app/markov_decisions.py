import time
import numpy as np

def relative_value_iteration_average_reward(TPM, TRM, s_ref, epsilon, max_iterations=10000, max_time=2.0):
    
    validate_tpm_stochastic(TPM)

    n, _, A = TPM.shape

    h = np.zeros(n)
    pi_star = np.zeros(n, dtype=int)
    iter_count = 0
    start = time.perf_counter()
    converged = False

    while True:
        iter_count += 1
        # Vectorized Bellman update
        R_plus_h = TRM + h[:, None, None]
        Q = np.sum(TPM * R_plus_h, axis=1)

        pi_star = np.argmin(Q, axis=1)
        h_new = Q[np.arange(n), pi_star]

        g_new = h_new[s_ref]
        h_new = h_new - g_new

        if np.max(np.abs(h_new - h)) < epsilon:
            converged = True
            return h_new, g_new, pi_star, iter_count, converged
        
        if time.perf_counter() - start > max_time:
            return h, g_new, pi_star, iter_count, converged
        
        if iter_count >= max_iterations:
            return h, g_new, pi_star, iter_count, converged

        h = h_new

def validate_tpm_stochastic(TPM: np.ndarray, tol: float = 1e-8) -> None:
    """
    Validate that a Transition Probability Matrix (TPM) is a proper
    stochastic kernel of shape (n, n, A).

    Checks:
    - TPM is 3D
    - TPM is square in the first two dimensions
    - All probabilities are non-negative
    - Each row for each action sums to 1 (within tolerance)

    Raises:
        ValueError: if any validation rule is violated.
    """
    if TPM.ndim != 3:
        raise ValueError(f"TPM must be 3-dimensional (n, n, A). Got shape {TPM.shape}")

    n, n2, A = TPM.shape

    # Check square structure
    if n != n2:
        raise ValueError(f"TPM must be square in the first two dimensions. Got {n}x{n2}")

    # Check non-negativity
    if np.any(TPM < 0):
        idx = np.unravel_index(np.argmin(TPM), TPM.shape)
        raise ValueError(f"TPM contains negative probability at index {idx}")

    # Check row sums for each state i and action a
    row_sums = TPM.sum(axis=1)  # shape (n, A)

    for i in range(n):
        for a in range(A):
            if abs(row_sums[i, a] - 1.0) > tol:
                raise ValueError(
                    f"TPM row for state {i}, action {a} must sum to 1. "
                    f"Got {row_sums[i, a]}"
                )
