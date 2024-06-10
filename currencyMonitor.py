import logging
from time import sleep
import random
import requests

logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level
)

logger = logging.getLogger('CurrencyMonitor')

def getCurrencyConversionRates(orig_currency: str, dest_currency: str, api_key: str) -> int:
    url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/{orig_currency}'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        conversion_rate = data['conversion_rates'][dest_currency]
        logging.debug(f"Conversion rate from {orig_currency} to {dest_currency}: {conversion_rate}")

    return conversion_rate

currency_rates = []


sample_rate_sec = 1
sample_interval_sec = 2
api_key = 'e811708c87af40b8525b1aa8'
orig_currency = 'USD'
dest_currency = 'EUR'

while sample_interval_sec > 0:
    logging.debug("Sampling API")
    currency_rates.append(getCurrencyConversionRates(orig_currency, dest_currency, api_key))
    sleep(sample_rate_sec)
    sample_interval_sec = sample_interval_sec - sample_rate_sec
logging.debug(f"Curreny values {currency_rates}")