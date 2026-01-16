from math import exp, comb
import pytest
from app.reliability import (
    exponential_reliability,
    mtbf_failure_rate_convert,
    series_system_reliability,
    kofn_system_reliability,
    validate_reliability_list
)

class TestExponentialReliability:
    """
    Test suite for the exponential_reliability function.
    """
    #Nominal Cases
    def test_exponential_reliability(self):
        """
        Tests the nominal behavior of the exponential_reliability function.
        """
        failure_rate = 0.001
        time = 1000
        result = exponential_reliability(failure_rate, time)
        assert round(result, 6) == round(exp(-failure_rate * time), 6)

    #Edge Cases
    def test_exponential_reliability_zero_time(self):
        """
        Tests the exponential_reliability function with zero mission time.
        """
        failure_rate = 0.001
        time = 0
        result = exponential_reliability(failure_rate, time)
        assert round(result, 6) == round(exp(-failure_rate * time), 6)
    
    def test_exponential_reliability_zero_failure_rate(self):
        """
        Tests the exponential_reliability function with zero failure rate.
        """
        failure_rate = 0.0
        time = 1000
        result = exponential_reliability(failure_rate, time)
        assert round(result, 6) == round(exp(-failure_rate * time), 6)

    #Invalid Cases
    def test_exponential_reliability_negative_time(self):
        """
        Tests the exponential_reliability function with negative mission time.
        """
        with pytest.raises(ValueError):
            exponential_reliability(0.1, -5)
        
    def test_exponential_reliability_negative_failure_rate(self):
        """
        Tests the exponential_reliability function with negative failure rate.
        """
        with pytest.raises(ValueError):
            exponential_reliability(-0.1, 15)

class TestMtbfFailureRateConvert:
    """
    Test suite for the mtbf_failure_rate_convert function.
    """
    def test_mtbf_failure_rate_convert_nominal(self):
        """
        Tests the mtbf_failure_rate_convert function with a nominal MTBF.
        """
        mtbf = 1000
        result = mtbf_failure_rate_convert(mtbf)
        assert round(result, 6) == round(1.0 / mtbf, 6)

    def test_mtbf_failure_rate_convert_negative(self):
        """
        Tests the mtbf_failure_rate_convert function with a negative MTBF.
        """
        mtbf = -1000
        with pytest.raises(ValueError):
            mtbf_failure_rate_convert(mtbf)

    def test_mtbf_failure_rate_convert_zero(self):
        """
        Tests the mtbf_failure_rate_convert function with a zero MTBF.
        """
        mtbf = 0
        with pytest.raises(ValueError):
            mtbf_failure_rate_convert(mtbf)

class TestSeriesSystemReliability:
    """
    Test suite for the series_system_reliability function.
    """
    def test_series_system_reliability_nominal(self):
        """
        Tests the series_system_reliability function with nominal component reliabilities.
        """
        component_reliabilities = [0.9, 0.95, 0.99]
        result = series_system_reliability(component_reliabilities)
        expected = 0.9 * 0.95 * 0.99
        assert round(result, 6) == round(expected, 6)

    def test_series_system_reliability_zero(self):
        """
        Tests the series_system_reliability function with a zero component reliability.
        """
        component_reliabilities = [0.9, 0.0, 0.99]
        with pytest.raises(ValueError):
            series_system_reliability(component_reliabilities)

    def test_series_system_reliability_negative(self):
        """
        Tests the series_system_reliability function with a negative component reliability.
        """
        component_reliabilities = [0.9, 0.95, -0.99]
        with pytest.raises(ValueError):
            series_system_reliability(component_reliabilities)

    def test_series_system_reliability_empty(self):
        """
        Tests the series_system_reliability function with a zero component reliability.
        """
        component_reliabilities = []
        with pytest.raises(ValueError):
            series_system_reliability(component_reliabilities)

class TestKofNSystemReliability:
    """
    Test suite for the kofn_system_reliability function.
        """
    def test_kofn_system_reliability_nominal_like_item(self):
        """
        Tests the kofn_system_reliability function with a nominal k-of-n system with like items.
        """
        reliability = 0.9
        min_required = 2
        component_reliabilities = [reliability, reliability, reliability, reliability]
        
        result = kofn_system_reliability(component_reliabilities, min_required)
        expected = 1 - (comb(4, 0) * (1 - reliability) ** 4 + comb(4, 1) * (1 - reliability) ** 3 * reliability)
        assert round(result, 6) == round(expected, 6)

    def test_kofn_system_reliability_empty(self):
        """
        Tests the kofn_system_reliability function with an empty component list.
        """
        component_reliabilities = []
        min_required = 2
        with pytest.raises(ValueError):
            kofn_system_reliability(component_reliabilities, min_required)

    def test_kofn_system_reliability_required_high(self):
        """
        Tests the kofn_system_reliability function with too many units required.
        """
        component_reliabilities = [0.9, 0.95, 0.99]
        min_required = 4
        with pytest.raises(ValueError):
            kofn_system_reliability(component_reliabilities, min_required)

    def test_kofn_system_reliability_required_negative(self):
        """
        Tests the kofn_system_reliability function with negative min_required.
        """
        component_reliabilities = [0.9, 0.95, 0.99]
        min_required = -1
        with pytest.raises(ValueError):
            kofn_system_reliability(component_reliabilities, min_required)

    def test_kofn_system_reliability_required_zero(self):
        """
        Tests the kofn_system_reliability function with zero min_required.
        """
        component_reliabilities = [0.9, 0.95, 0.99]
        min_required = 0
        with pytest.raises(ValueError):
            kofn_system_reliability(component_reliabilities, min_required)

    def test_kofn_system_reliability_zero_reliability(self):
        """
        Tests the kofn_system_reliability function with a zero component reliability.
        """
        component_reliabilities = [0.9, 0.0, 0.99]
        min_required = 2
        with pytest.raises(ValueError):
            kofn_system_reliability(component_reliabilities, min_required)
    
    def test_kofn_system_reliability_negative_reliability(self):
        """
        Tests the kofn_system_reliability function with a negative component reliability.
        """
        component_reliabilities = [0.9, -0.05, 0.99]
        min_required = 2
        with pytest.raises(ValueError):
            kofn_system_reliability(component_reliabilities, min_required)
    
    
    def test_kofn_system_reliability_dissimilar_items(self):
        component_reliabilities = [0.9, 0.8, 0.7]
        min_required = 2
        #manuallya calculate probability of at least 2 working
        three_good = 0.9 * 0.8 * 0.7 #all working
        two_good = (0.9 * 0.8 * (1 - 0.7) + # first two working
                    0.9 * (1 - 0.8) * 0.7 + # first and last working
                    (1 - 0.9) * 0.8 * 0.7) # last two working
        expected = three_good + two_good

        # Placeholder expected value — replace when implemented
        result = kofn_system_reliability(component_reliabilities, min_required)

        # This assertion is intentionally wrong for now
        assert round(result, 6) == round(expected, 6)


class TestValidateReliabilityList:
    def test_validate_reliability_list_negative(self):
        """
        Tests the validate_reliability_list function with a negative reliability value.
        """
        component_reliabilities = [0.9, -0.95, 0.99]
        with pytest.raises(ValueError):
            validate_reliability_list(component_reliabilities)

    def test_validate_reliability_list_zero(self):
        """
        Tests the validate_reliability_list function with a zero reliability value.
        """
        component_reliabilities = [0.9, 0, 0.99]
        with pytest.raises(ValueError):
            validate_reliability_list(component_reliabilities)

    def test_validate_reliability_list_high(self):
        """
        Tests the validate_reliability_list function with a reliability value greater than 1.
        """
        component_reliabilities = [0.9, 2, 0.99]
        with pytest.raises(ValueError):
            validate_reliability_list(component_reliabilities)

    def test_validate_reliability_list_empty(self):
        """
        Tests the validate_reliability_list function with an empty list.
        """
        component_reliabilities = []
        with pytest.raises(ValueError):
            validate_reliability_list(component_reliabilities)

