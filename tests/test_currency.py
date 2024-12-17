from datetime import timedelta
import pytest
from fastapi.testclient import TestClient
from aioresponses import aioresponses

from currency_exchange.app.core.security import create_jwt_token
from currency_exchange.main import api_v1_app

client = TestClient(api_v1_app)


def token_for_test():
    token_data = {"sub": "test_user"}
    return create_jwt_token(data=token_data, expires_delta=timedelta(minutes=30))


@pytest.fixture
def headers():
    token = token_for_test()
    headers = {"Authorization": f"Bearer {token}"}
    return headers


def test_get_list_currencies(headers: dict[str, str]) -> None:
    url = "https://api.apilayer.com/currency_data/list"
    mock_response = {
        "currencies": {
            "USD": "United States Dollar",
            "EUR": "Euro",
            "RUB": "Russian Ruble",
        }
    }

    with aioresponses() as m:
        m.get(url, payload=mock_response)

        response = client.get("/currency/list/", headers=headers)

        assert response.status_code == 200
        response_json = response.json()
        assert isinstance(response_json, dict)
        assert "USD" in response_json
        assert "EUR" in response_json
        assert "RUB" in response_json
        assert response_json["USD"] == "United States Dollar"
        assert response_json["EUR"] == "Euro"
        assert response_json["RUB"] == "Russian Ruble"


class TestConvertCurrency:
    @pytest.mark.asyncio
    def test_get_convert_currency(self, headers: dict[str, str]):
        currency_data = {"to_currency": "USD", "from_currency": "EUR", "amount": 100}
        url = (
            "https://api.apilayer.com/currency_data/convert?to=USD&from=EUR&amount=100"
        )

        with aioresponses() as m:
            m.get(url, payload={"result": 120.0})

            response = client.post(
                "/currency/exchange/", json=currency_data, headers=headers
            )

            assert response.status_code == 200
            response_json = response.json()
            assert isinstance(response_json, dict)
            assert "total" in response_json
            assert response_json["total"] == 120.0

    @pytest.mark.asyncio
    async def test_get_convert_currency_key_error(self, headers: dict[str, str]):
        currency = {"to_currency": "INVALID", "from_currency": "EUR", "amount": 100}
        url = "https://api.apilayer.com/currency_data/convert?to=INVALID&from=EUR&amount=100"

        with aioresponses() as m:
            m.get(url, payload={})

            response = client.post(
                "/currency/exchange/", json=currency, headers=headers
            )
            assert response.status_code == 200
            response_json = response.json()
            assert isinstance(response_json, dict)
            assert "error" in response_json
            assert (
                response_json["error"]
                == "Для просмотра допустимых код валют перейдите в /list."
            )
