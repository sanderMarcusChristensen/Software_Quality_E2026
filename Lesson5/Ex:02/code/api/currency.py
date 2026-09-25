import json
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class Currency:
    """Convert money using current exchange rates from freecurrencyapi.com."""

    def __init__(self, base_currency):
        if len(base_currency) != 3 or not base_currency.isalpha():
            raise ValueError("Base currency must be a 3-letter code, such as 'DKK'.")

        self.base_currency = base_currency.upper()

    def convert(self, amount, destination_currency):
        """Convert an amount to another 3-letter currency code."""
        if len(destination_currency) != 3 or not destination_currency.isalpha():
            raise ValueError("Destination currency must be a 3-letter code.")

        destination_currency = destination_currency.upper()
        api_key = os.environ.get("FREECURRENCYAPI_KEY")
        if not api_key:
            raise ValueError("Set the FREECURRENCYAPI_KEY environment variable first.")

        # The latest endpoint returns rates for the chosen base currency.
        parameters = urlencode({"base_currency": self.base_currency})
        url = "https://api.freecurrencyapi.com/v1/latest?" + parameters
        request = Request(url, headers={"apikey": api_key})

        with urlopen(request, timeout=10) as response:
            rates = json.load(response)["data"]

        if destination_currency not in rates:
            raise ValueError("The destination currency is not supported by the API.")

        rate = rates[destination_currency]
        return round(round(amount, 2) * rate, 2)
