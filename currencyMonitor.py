import logging
from time import sleep
import requests
import numpy as np
import argparse
import sys

logger = None


def get_logger(filename: str, log_level=logging.INFO):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.FileHandler(filename, mode="w+"), logging.StreamHandler()],
    )
    logger = logging.getLogger("CurrencyMonitor")
    return logger


def getCurrencyConversionRates(
    base_currency: str, dest_currency: str, api_key: str
) -> int:
    api_url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            if dest_currency not in data["conversion_rates"]:
                logger.error(
                    f"{dest_currency} currency exchange rate was "
                    f"not listed for {base_currency}"
                )
                return None
            conversion_rate = data["conversion_rates"][dest_currency]
            conversion_rate_log_string = (
                f"Conversion rate from "
                f"{base_currency} to {dest_currency} :"
                f"{conversion_rate}"
            )
            logger.info(conversion_rate_log_string)
            print(conversion_rate_log_string)  # For the assigment
            return conversion_rate
        else:
            logger.error(f"Respose failed with status code" f"{response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Failure to reach  {api_url}, " f"failed with expecption {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="A simple program to \
                                    show the currency rates",
        add_help=True,
    )
    parser.add_argument(
        "-f",
        "--log_file",
        type=str,
        default="currencymonitor.log",
        help="Logging File name",
    )
    parser.add_argument(
        "-b",
        "--base_currency",
        type=str,
        default="USD",
        help="Base currency to exchange from",
    )
    parser.add_argument(
        "-d",
        "--dest_currency",
        type=str,
        default="EUR",
        help="Destination currency to exchange to",
    )
    parser.add_argument(
        "-a",
        "--api_key",
        type=str,
        default="e811708c87af40b8525b1aa8",
        help="API key to \
                        https://app.exchangerate-api.com/dashboard",
    )
    parser.add_argument(
        "--sample_rate",
        type=int,
        default="5",
        help="Sample rate to \
                        get the exchange currency values in seconds",
    )
    parser.add_argument(
        "--duration",
        type=int,
        default="60",
        help="Overall duration for \
                         sampling the exchange rate in seconds",
    )
    # Parse the arguments
    args = parser.parse_args()
    log_file = args.log_file
    global logger
    logger = get_logger(log_file)
    sample_rate_sec = args.sample_rate
    sample_interval_sec = args.duration
    api_key = args.api_key
    base_currency = args.base_currency
    dest_currency = args.dest_currency
    if sample_interval_sec <= sample_rate_sec:
        logger.error("Duration shorter that sample rate")
        sys.exit(1)
    currency_rates = np.array([])
    average_logger_bool = False
    timer = 0
    while sample_interval_sec > 0:
        logger.debug("Sampling API")
        if timer >= 60:
            average_logger_bool = True
            logger.info(
                f"Average Current Exchange rate in last 60  "
                f"seconds between {base_currency} and {dest_currency} "
                f"is {np.average(currency_rates)}"
            )
            timer = 0
        exchange_rate = getCurrencyConversionRates(
            base_currency, dest_currency, api_key
        )
        if exchange_rate:
            currency_rates = np.append(currency_rates, exchange_rate)
        else:
            logger.debug(
                "Current Exchange rate while calculating average  "
                "since there had been an error"
            )
        sleep(sample_rate_sec)
        timer = timer + sample_rate_sec
        sample_interval_sec = sample_interval_sec - sample_rate_sec
    if not average_logger_bool:
        logger.info(
            f"Average exchange rate over {args.duration} "
            f"seconds is {np.average(currency_rates)}"
        )


if __name__ == "__main__":
    main()
