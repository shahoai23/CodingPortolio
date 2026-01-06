from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestExponentialReliabilityAPI:
    """
    Test suite for the Exponential Reliability API endpoint.
    """
    def test_exponential_reliability_api_nominal(self):
        response = client.post(
            "/reliability/exponential",
            json={"failure_rate": 0.001, "mission_time": 1000}
        )
        assert response.status_code == 200
        data = response.json()
        assert "reliability" in data

    def test_exponential_reliability_api_negative_time(self):
        response = client.post(
            "/reliability/exponential",
            json={"failure_rate": 0.1, "mission_time": -5}
        )
        assert response.status_code == 422

class TestMtbfConversionAPI:
    """
    Test suite for the MTBF Conversion API endpoint.
    """
    def test_mtbf_conversion_api_nominal(self):
        response = client.post(
            "/reliability/mtbf-convert",
            json={"value": 1000}
        )
        assert response.status_code == 200
        data = response.json()
        assert "converted_value" in data

    def test_mtbf_conversion_api_negative_value(self):
        response = client.post(
            "/reliability/mtbf-convert",
            json={"value": -1000}
        )
        assert response.status_code == 422

class TestSeriesSystemAPI:
    """
    Test suite for the Series System Reliability API endpoint.
    """
    def test_series_system_api_nominal(self):
        response = client.post(
            "/reliability/series",
            json={"component_reliabilities": [0.9, 0.95, 0.99]}
        )
        assert response.status_code == 200
        data = response.json()
        assert "reliability" in data

    def test_series_system_api_invalid_reliability(self):
        response = client.post(
            "/reliability/series",
            json={"component_reliabilities": [0.9, 1.05, 0.99]}
        )
        assert response.status_code == 422

class TestKofNSystemAPI:
    """
    Test suite for the k-of-n System Reliability API endpoint.
    """
    def test_kofn_system_api_nominal_like_item(self):
        response = client.post(
            "/reliability/kofn",
            json={"component_reliabilities": [0.9, 0.9, 0.9], "min_required": 2}
        )
        assert response.status_code == 200
        data = response.json()
        assert "reliability" in data

    def test_kofn_system_api_invalid_min_required(self):
        response = client.post(
            "/reliability/kofn",
            json={"component_reliabilities": [0.9, 0.9, 0.9], "min_required": 0}
        )
        assert response.status_code == 422