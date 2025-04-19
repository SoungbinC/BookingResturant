import httpx
from main import app


def test_example():
    with httpx.Client(app=app) as client:
        response = client.get("/some-endpoint")
        assert response.status_code == 200
