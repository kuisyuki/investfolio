import requests
from typing import Optional

class ExchangeRateClient:
    def __init__(self):
        # Note: This endpoint uses HTTP, not HTTPS.
        self.api_url = "http://www.floatrates.com/daily/usd.json"

    def get_usd_jpy_rate(self) -> Optional[float]:
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()
            # The response is a dictionary of currencies, we need to get the 'jpy' item.
            if "jpy" in data and "rate" in data["jpy"]:
                return data["jpy"]["rate"]
            else:
                print("Rate for JPY not found in FloatRates response")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching from FloatRates: {e}")
            return None
        except (KeyError, TypeError, ValueError) as e:
            print(f"Error parsing response from FloatRates: {e}")
            return None
