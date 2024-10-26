# **JaxEPICS Permit Scraper**

---

## Overview

The **JaxEPICS Permit Data Scraper** is a Python-based tool designed to automate the extraction of permit data from the City of Jacksonville's EPICS (Electronic Plan Information and Communication System) API. This tool allows users to specify a date range and retrieve detailed permit information, including additional details such as job cost, company information, and contractor details. The script is robust, featuring comprehensive logging, error handling, and modular code architecture for ease of maintenance and scalability.

---

## Features

- **Date Range Filtering**: Specify custom start and end dates to filter permits by their issue dates.
- **Data Extraction**: Retrieves permit data, including detailed company and contractor information.
- **Data Processing**: Cleans and structures the data, renaming and reordering columns as needed.
- **Output Formats**: Saves the extracted data in both JSON and Excel (`.xlsx`) formats.
- **Logging**: Provides detailed logs both in the console and in a log file for monitoring and debugging.
- **Error Handling**: Includes robust error handling to ensure the script continues running even if some records fail.
- **Modularity**: Organized code structure with separate modules for configuration, API interactions, and data processing.

---

## Directory Structure

```
jaxepics_permit_scraper/
├── main.py
├── config.py
├── api.py
├── data_processing.py
├── requirements.txt
└── README.md
```

---

## Requirements

- **Python 3.6+**
- **Packages**:
  - `requests`
  - `pandas`
  - `openpyxl`
  - `tqdm`

---

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/jaxepics_permit_scraper.git
   cd jaxepics_permit_scraper
   ```

2. **Create a Virtual Environment** (Optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```
---
## Usage

Run the script using the following command, providing the start date and end date as arguments in YYYY-MM-DD format:
```bash
python main.py START_DATE END_DATE
```
**Example:**
```bash
python main.py 2024-10-24 2024-10-25
```
**Note**: The script will output logs to both the console and a log file named after the date range (e.g., `20241024_20241025.log`).

---

## Output

- **JSON File**: Contains the raw data retrieved from the API.
  - Filename: `YYYYMMDD_YYYYMMDD.json` (e.g., `20241024_20241025.json`)
- **Excel File**: Contains the processed and formatted data.
  - Filename: `YYYYMMDD_YYYYMMDD.xlsx` (e.g., `20241024_20241025.xlsx`)
- **Log File**: Detailed logs of the script's execution.
  - Filename: `YYYYMMDD_YYYYMMDD.log` (e.g., `20241024_20241025.log`)

---

## Logging and Monitoring

- The script provides real-time feedback in the console, including progress bars and detailed logging messages.
- All logs are also saved to a log file for later review.

---

## Error Handling

- The script includes robust error handling to ensure that it continues running even if some records fail to process.
- Exceptions and errors are logged with detailed stack traces to facilitate debugging.

---

## Customization

- **Adjusting the Delay Between Requests**:
  - Located in `data_processing.py`, you can adjust the `time.sleep(0.1)` delay to control the rate of API requests.
- **Modifying Log Levels**:
  - In `main.py`, you can change the logging level in the `logging.basicConfig` setup.

---

## Code Structure

- **`main.py`**: The entry point of the script; orchestrates the workflow.
- **`config.py`**: Contains configuration variables such as date ranges and filename base.
- **`api.py`**: Handles all interactions with the API, including fetching permit listings and details.
- **`data_processing.py`**: Manages data manipulation, processing, and saving.
- **`requirements.txt`**: Lists all Python dependencies required to run the script.

---

## Dependencies

- **requests**: For making HTTP requests to the API.
- **pandas**: For data manipulation and processing.
- **openpyxl**: For writing data to Excel files.
- **tqdm**: For displaying progress bars in the console.

---

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes or improvements.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Disclaimer

- This tool is intended for educational and informational purposes.
- Please ensure you comply with all applicable laws and regulations when using this script.
- Be mindful of the API's usage policies to avoid overloading the server.

---

## Contact

For questions or support, please contact [yourname@example.com](mailto:yourname@example.com).

---

## Acknowledgments

- Thanks to the City of Jacksonville for providing access to the EPICS API.
- Inspired by the need for efficient data extraction and processing tools.

---

**Enjoy using the JaxEPICS Permit Data Scraper!**