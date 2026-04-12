import pytest

@pytest.fixture
def mock_api_response():
    return {
        "status": "success",
        "code": 200,
        "data": {
            "id": 1,
            "name": "Mahesh"
        }
    }

def test_status_code(mock_api_response):
    assert mock_api_response["code"] == 200

def test_required_keys(mock_api_response):
    assert "status" in mock_api_response
    assert "code" in mock_api_response
    assert "data" in mock_api_response