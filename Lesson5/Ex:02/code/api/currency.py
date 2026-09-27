import os

import currencyapicom
from dotenv import load_dotenv


class Currency:
    """Omregner penge med kurser fra currencyapi.com."""

    def __init__(self, base_currency):
        if len(base_currency) != 3 or not base_currency.isalpha():
            raise ValueError("Base currency must be a 3-letter code, such as 'DKK'.")

        self.base_currency = base_currency.upper()

        # Find .env automatisk og læs API-nøglen.
        load_dotenv()
        api_key = os.environ.get("LESSON5_CURRENCY_API_KEY")
        if not api_key:
            raise ValueError("Set LESSON5_CURRENCY_API_KEY in the project's .env file.")

        # Klienten sender vores forespørgsler til API'et.
        self.client = currencyapicom.Client(api_key)

    def currencies(self):
        """Hent oplysninger om alle understøttede valutaer."""
        return self.client.currencies()

    def convert(self, amount, destination_currency):
        """Omregn et beløb fra basisvalutaen til den ønskede valuta."""
        if len(destination_currency) != 3 or not destination_currency.isalpha():
            raise ValueError("Destination currency must be a 3-letter code.")

        destination_currency = destination_currency.upper()

        # Hent alle kurser for vores basisvaluta, fx DKK.
        response = self.client.latest(base_currency=self.base_currency)
        rates = response["data"]

        if destination_currency not in rates:
            raise ValueError("The destination currency is not supported by the API.")

        # Find kursen for den ønskede valuta, fx USD.
        exchange_rate = rates[destination_currency]["value"]

        # Afrund beløbet, omregn det og afrund resultatet.
        amount = round(amount, 2)
        converted_amount = amount * exchange_rate
        return round(converted_amount, 2)
