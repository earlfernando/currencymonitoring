import logging
from time import sleep
import requests
import numpy as np
import argparse
import sys
from datetime import date

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
    api_url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={base_currency}&to_currency={dest_currency}&apikey={api_key}"  # noqa
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            conversion_rate = data["Realtime Currency Exchange Rate"][
                "5. Exchange Rate"
            ]
            conversion_rate_log_string = (
                f"Conversion rate from "
                f"{base_currency} to {dest_currency} :"
                f"{conversion_rate}"
            )
            logger.debug(conversion_rate_log_string)
            now = date.today()
            date_time_string = now.strftime("%d/%m/%Y %H:%M:%S")
            print(date_time_string, conversion_rate_log_string)  # For the assigment
            return conversion_rate
        else:
            logger.error(f"Respose failed with status code" f"{response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Failure to reach  {api_url}, " f"failed with expecption {e}")
        return None
    except KeyError as e:
        logger.error(
            f"Failure to get the conversion rates from {base_currency} to "
            f"{dest_currency}  falied with exception {e}"
        )
        sys.exit(1)


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
        default="SAG2FIHV7V60IO6I",
        help="API key to \
                        https://www.alphavantage.co",
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
            if len(currency_rates) == 0:
                logger.info(
                    "Currency exchange rates were not captured in the last"
                    " 60 seconds due to errors"
                )
            else:
                logger.info(
                    f"Average Current Exchange rate in last 60  "
                    f"seconds between {base_currency} and {dest_currency} "
                    f"is {np.average(currency_rates)}"
                )
            timer = 0
            currency_rates = np.array([])
        exchange_rate = getCurrencyConversionRates(
            base_currency, dest_currency, api_key
        )
        if exchange_rate:
            currency_rates = np.append(currency_rates, exchange_rate)
        else:
            logger.debug(
                "Skipping current Exchange rate while calculating average  "
                "since there had been an error"
            )
        sleep(sample_rate_sec)
        timer = timer + sample_rate_sec
        sample_interval_sec = sample_interval_sec - sample_rate_sec
    if not average_logger_bool:
        if len(currency_rates) == 0:
            logger.warning(
                "Currency Exchange rates were not captured in the last"
                "60 seconds due to errors"
            )
        else:
            logger.info(
                f"Average exchange rate over {args.duration} "
                f"seconds is {np.average(currency_rates)}"
            )


if __name__ == "__main__":
    main()
