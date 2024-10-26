import logging
import time
import math
import argparse
from api import get_results, get_permit_details
from data_processing import (
    process_initial_data,
    process_permit_details,
    save_to_excel,
    save_to_json,
)
from config import BANNER, setup_config

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='JaxEPICS Permit Data Scraper')
    parser.add_argument('start_date', type=str, help='Start date in YYYY-MM-DD format')
    parser.add_argument('end_date', type=str, help='End date in YYYY-MM-DD format')
    args = parser.parse_args()

    # Set up configuration with the provided dates
    config = setup_config(args.start_date, args.end_date)

    # Configure logging to output to both file and console
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(f"{config['filename_base']}.log", mode='w'),
            logging.StreamHandler()
        ]
    )
    print(BANNER)
    time.sleep(2)
    logging.info("Scraper started.")

    # Initial request to get the total count
    try:
        logging.debug("Sending initial request to get total count.")
        initial_data = get_results(1, 10, config)
        if initial_data:
            count = initial_data.get("count", 0)
            logging.info(f"Total number of results: {count}")
            if count == 0:
                logging.warning("No results found for the given date range.")
                return
            if count < 20000:
                logging.info("Fetching all results in a single request.")
                result_data = get_results(1, count, config)
                if result_data and "values" in result_data:
                    df = process_initial_data(result_data["values"])
                    df = process_permit_details(df)
                    save_to_json(result_data, config['filename_base'])
                    save_to_excel(df, config['filename_base'])
                else:
                    logging.error("No 'values' found in response.")
            else:
                logging.info("Fetching results in multiple requests due to large data size.")
                num_pages = math.ceil(count / 20000)
                all_values = []
                for page in range(1, num_pages + 1):
                    logging.info(f"Fetching page {page} of {num_pages}")
                    result_data = get_results(page, 20000, config)
                    if result_data and "values" in result_data:
                        all_values.extend(result_data["values"])
                    else:
                        logging.error(f"No 'values' found in response for page {page}")
                        break
                if all_values:
                    df = process_initial_data(all_values)
                    df = process_permit_details(df)
                    save_to_json({"values": all_values}, config['filename_base'])
                    save_to_excel(df, config['filename_base'])
                else:
                    logging.error("No data collected.")
        else:
            logging.error("Failed to get initial data.")
    except Exception as e:
        logging.exception("An unexpected error occurred.")
    finally:
        logging.info("Script finished.")

if __name__ == "__main__":
    main()
