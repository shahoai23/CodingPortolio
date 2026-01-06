from math import exp
from typing import Literal

def exponential_reliability(failure_rate: float, time: float) -> float:
    """
    Calculate the reliability of an element using the exponential reliability function.

    Parameters:
    failure_rate (float): The failure rate (λ) of the system.
    time (float): The time period over which to calculate reliability.

    Returns:
    float: The reliability of the system at the given time.

    Ground Rules, Assumptions, and Limitations:
    1. The item must have a time to fail distribution that is exponential for this to be applicable (i.e. constant failure rate).
        a. Not applicable for items which exhibit wear-out or infant mortality.
    2. Never applicable to parallel systems. You can have potentially acceptable error if mission length is << MTBF.
    

    """
    if failure_rate < 0:
        raise ValueError("Failure rate must be non-negative.")
    if time < 0:
        raise ValueError("Time must be non-negative.")
    
    return exp(-failure_rate * time)

def mtbf_failure_rate_convert(value: float) -> float:
    """
    Convert MTBF to failure rate or failure rate to MTBF.
    
    Parameters:
    value (float): The MTBF (Mean Time Between Failures) or failure rate (λ).

    Returns:
    float: the corresponding failure rate if MTBF is given, or MTBF if failure rate is given.

    Ground Rules, Assumptions, and Limitations:
    1. MTBF and failure rate are reciprocals of each other (exponential distribution assumption).
    2. Value must be positive.
    """
    if value < 0:
        raise ValueError("Value must be positive.")
    
    return 1.0 / value

def series_system_reliability(component_reliabilities: list[float]) -> float:
    """
    Calculate the reliability of a series system.

    Parameters:
    component_reliabilities (list[float]): A list of reliabilities for each component in the series system.

    Returns:
    float: The overall reliability of the series system.

    Ground Rules, Assumptions, and Limitations:
    1. All components must be in series configuration.
    2. Component failures are assumed to be independent events.
    3. Duty cycling, time, or other factors are already accounted for in the component reliability values.
    4. Component reliabilities must be between 0 and 1 (exclusive of 0, inclusive of 1).
    """
    #validate reliabilities are between 0 and 1
    validate_reliability_list(component_reliabilities)
   
    system_reliability = 1.0
    for reliability in component_reliabilities:
        system_reliability *= reliability
    return system_reliability

def kofn_system_reliability(component_reliabilities: list[float], min_required: int) -> float:
    """
    Calculate the reliability of a k-of-n system.

    Parameters:
    component_reliabilities (list[float]): A list of reliabilities for each component in the k-of-n system.

    Returns:
    float: The overall reliability of the k-of-n system.

    Ground Rules, Assumptions, and Limitations:
    1. All components must be in parallel configuration.
    2. Component failures are assumed to be independent events.
    3. Duty cycling, time, or other factors are already accounted for in the component reliability values.
    4. Component reliabilities must be between 0 and 1 (exclusive of 0, inclusive of 1).
    5. Switching probability is 100% (i.e., no failure in switching between components).
    """
    #validate reliabilities are between 0 and 1
    validate_reliability_list(component_reliabilities)
    
    if min_required < 1 or min_required > len(component_reliabilities):
        raise ValueError("min_required must be between 1 and the number of components.")
    
    if len(set(component_reliabilities)) == 1:
        # All reliabilities are the same, use simplified formula
        r = component_reliabilities[0]
        n = len(component_reliabilities)
        k = min_required
        system_reliability = 0

        from math import comb
        system_reliability = sum(comb(n, i) * (r ** i) * ((1 - r) ** (n - i)) for i in range(k, n + 1))
        
        return system_reliability
    else: #TODO: Implement general case for dissimilar redundancy
        raise NotImplementedError("Parallel system reliability for dissimilar component reliabilities is not yet implemented.")

def validate_reliability_list(reliabilities: list[float]) -> None:
    """
    Helper function to validate that reliabilities are valid for use.
    
    :param reliabilities: Description
    :type reliabilities: list[float]
    """
    if not reliabilities:
        raise ValueError("Component reliabilities list cannot be empty.")
    if any(r <= 0 or r > 1 for r in reliabilities):
        raise ValueError("All component reliabilities must be between 0 and 1.")    