import logging
from time import sleep
import random
import requests
import numpy as np
import argparse

logger = None

def get_logger(filename:str, log_level = logging.INFO):
    logging.basicConfig(
        level=logging.INFO,  # Set the logging level
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Set the logging format
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
        logging.FileHandler(filename),  # Log to a file named app.log
        logging.StreamHandler()  # Optionally, also log to the console
])

    logger = logging.getLogger('CurrencyMonitor')
    return logger

def getCurrencyConversionRates(orig_currency: str, dest_currency: str, api_key: str) -> int:
    url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/{orig_currency}'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        conversion_rate = data['conversion_rates'][dest_currency]
        logging.info(f"Conversion rate from {orig_currency} to {dest_currency}: {conversion_rate}")

    return conversion_rate

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="A simple program to show the currency rates", add_help=True)
    parser.add_argument('-f', '--log_file', type=str, default = "currencymonitor.log", help='Logging File name')
    
    # Parse the arguments
    args = parser.parse_args()
    log_file = args.log_file
    logger = get_logger(log_file)

    sample_rate_sec = 1
    sample_interval_sec = 2
    api_key = 'e811708c87af40b8525b1aa8'
    orig_currency = 'USD'
    dest_currency = 'EUR'

    currency_rates = np.array([])
    while sample_interval_sec > 0:
        logging.debug("Sampling API")
        #currency_rates = np.append(currency_rates,random.random())
        currency_rates = np.append(currency_rates,getCurrencyConversionRates(orig_currency, dest_currency, api_key))
        #currency_rates.append(getCurrencyConversionRates(orig_currency, dest_currency, api_key))
        sleep(sample_rate_sec)
        sample_interval_sec = sample_interval_sec - sample_rate_sec
    logger.info(f"Average of over 60 seconds {np.average(currency_rates)}")

if __name__ == '__main__':
    main()

