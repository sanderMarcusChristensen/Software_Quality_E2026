from unittest.mock import Mock

import pytest
import requests
from everapi.exceptions import ApiError

import currency
from currency import Currency


@pytest.fixture(autouse=True)
def api_client(monkeypatch):
    """Alle tests får en fake klient og nøgle; ingen rigtig .env eller internet."""
    client = Mock(spec=currency.currencyapicom.Client)
    client.latest.return_value = {
        "data": {
            "DKK": {"value": 1},
            "USD": {"value": 0.15},
            "EUR": {"value": 0.13},
        }
    }

    monkeypatch.setattr(currency, "load_dotenv", lambda: None)
    monkeypatch.setenv("LESSON5_CURRENCY_API_KEY", "test-key")
    monkeypatch.setattr(currency.currencyapicom, "Client", Mock(return_value=client))

    def block_network(*args, **kwargs):
        pytest.fail("Unit tests må ikke sende rigtige HTTP-kald.")

    monkeypatch.setattr(requests.sessions.Session, "request", block_network)
    return client


# (beløb, basisvaluta, destination, fast kurs, forventet resultat)
valid_cases = [
    (100, "DKK", "USD", 0.15, 15.00),
    (10.5, "DKK", "USD", 2, 21.00),
    (10.25, "DKK", "USD", 2, 20.50),
    (10, "DKK", "USD", 0.13456, 1.35),
    (0.01, "DKK", "USD", 0.15, 0.00),
    (0, "DKK", "USD", 0.15, 0.00),
    (25, "DKK", "DKK", 1, 25.00),
    (100, "dkk", "usd", 0.15, 15.00),
    (100, "EUR", "USD", 1.1, 110.00),
    (100, "USD", "EUR", 0.9, 90.00),
]


@pytest.mark.parametrize("amount, base, destination, rate, expected", valid_cases)
def test_valid_conversion(amount, base, destination, rate, expected, api_client):
    # Arrange: den første kurs er bevidst ikke den ønskede destination.
    api_client.latest.return_value = {
        "data": {
            "JPY": {"value": 99},
            destination.upper(): {"value": rate},
        }
    }
    converter = Currency(base)

    # Act
    result = converter.convert(amount, destination)

    # Assert
    assert result == expected
    api_client.latest.assert_called_once_with(base_currency=base.upper())


invalid_codes = ["DK", "DKKK", "", "D1K", "D K", None, 123]


@pytest.mark.parametrize("code", invalid_codes)
def test_invalid_base_currency(code, api_client):
    # Arrange
    expected_error = ValueError

    # Act: pytest.raises kontrollerer samtidig den forventede fejl.
    with pytest.raises(expected_error):
        Currency(code)

    # Assert
    api_client.latest.assert_not_called()


@pytest.mark.parametrize("code", invalid_codes)
def test_invalid_destination_currency(code, api_client):
    # Arrange
    converter = Currency("DKK")

    # Act
    with pytest.raises(ValueError):
        converter.convert(100, code)

    # Assert
    api_client.latest.assert_not_called()


invalid_amounts = [
    -1, -0.01, 10.251, "abc", None, True,
    float("inf"), float("-inf"), float("nan"),
]


@pytest.mark.parametrize("amount", invalid_amounts)
def test_invalid_amount(amount, api_client):
    # Arrange
    converter = Currency("DKK")

    # Act
    with pytest.raises(ValueError):
        converter.convert(amount, "USD")

    # Assert
    api_client.latest.assert_not_called()


@pytest.mark.parametrize("data", [{"EUR": {"value": 0.13}}, {}])
def test_destination_missing_from_response(data, api_client):
    # Arrange
    api_client.latest.return_value = {"data": data}
    converter = Currency("DKK")

    # Act
    with pytest.raises(ValueError) as error:
        converter.convert(100, "USD")

    # Assert
    assert str(error.value) == "The destination currency is not supported by the API."


def test_unsupported_base_currency(api_client):
    # Arrange: ZZZ er valgt som en ukendt kode i vores fake API.
    api_client.latest.side_effect = ApiError("Unsupported base currency")
    converter = Currency("ZZZ")

    # Act
    with pytest.raises(ApiError) as error:
        converter.convert(100, "USD")

    # Assert
    assert str(error.value) == "Unsupported base currency"
    api_client.latest.assert_called_once_with(base_currency="ZZZ")


def test_missing_api_key(monkeypatch, api_client):
    # Arrange: fixture-funktionen har også deaktiveret indlæsning af .env.
    monkeypatch.delenv("LESSON5_CURRENCY_API_KEY")

    # Act
    with pytest.raises(ValueError) as error:
        Currency("DKK")

    # Assert
    assert "LESSON5_CURRENCY_API_KEY" in str(error.value)
    api_client.latest.assert_not_called()
