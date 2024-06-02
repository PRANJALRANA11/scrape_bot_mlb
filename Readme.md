# Baseball Scores Scraper  -- Daily data scraper script

## Overview

This script scrapes the latest baseball scores from [Baseball Monster](https://baseballmonster.com/boxscores.aspx) and uploads the data to a Google Sheets spreadsheet. The script is designed to run daily, fetching the most recent scores and updating the spreadsheet accordingly.

## Features

- Scrapes batting and pitching data from Baseball Monster.
- Identifies the opponent team and determines win/loss for each player.
- Updates a specified Google Sheets spreadsheet with the scraped data.
- Automatically handles Google Sheets API authentication.
- Includes the date of the previous day for each row of data.

## Requirements

- Python 3.6+
- Google Cloud project with Sheets API enabled
- `cred.json` file for Google Sheets API credentials

## Installation

1. Clone the repository or download the script.

2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Google Sheets API credentials:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project and enable the Google Sheets API.
   - Create OAuth 2.0 credentials and download the `cred.json` file.
   - Save the `cred.json` file in the same directory as the script.

4. Run the script to authenticate and generate the `token.json` file:
   ```bash
   python mlb_scraper.py
   ```

## Usage

To run the script, simply execute:
```bash
python mlb_scraper.py
```

The script will:
- Authenticate with Google Sheets API.
- Scrape the latest baseball scores from Baseball Monster.
- Append the scraped data to the specified Google Sheets spreadsheet.

## Script Details

### Functions

- `main()`: Orchestrates the scraping and uploading process.
- `write_match_data(ws_id, match_data, headers)`: Writes the match data to the specified worksheet in the Google Sheets.
- `add_worksheet(title)`: Adds a new worksheet to the Google Sheets.

### Authentication

The script uses OAuth 2.0 for authentication. The first time you run the script, it will prompt you to log in to your Google account and authorize access. The credentials are then saved in `token.json` for future runs.

### Data Processing

- The script fetches the webpage content using `requests` and parses it with `BeautifulSoup`.
- It processes batting and pitching tables, extracting relevant data.
- The date is set to the previous day using the `datetime` module.
- The opponent team and win/loss information are determined using regex matching.

### Google Sheets Integration

- The script uses the `google-api-python-client` library to interact with Google Sheets.
- It appends the scraped data to the specified worksheet in the spreadsheet.

## Customization

- **Spreadsheet ID**: Change the `spreadsheet_id` variable in the script to the ID of your Google Sheets spreadsheet.
- **Worksheet Titles**: Modify the `add_worksheet` function to set custom titles for the worksheets.

## Error Handling

The script includes basic error handling for HTTP and Google Sheets API errors. If an error occurs, it will be printed to the console.








# Baseball Data Scraper   ----- Previous data scraper (from season starts)

## Overview

This script is designed to scrape historical baseball data from [Baseball Monster](https://baseballmonster.com/boxscores.aspx) using Selenium and BeautifulSoup. The scraped data is then stored in an Excel file with separate sheets for batting and pitching data.

## Features

- Uses Selenium to navigate and interact with the web page.
- Scrapes both batting and pitching data for historical matches.
- Saves the scraped data in an Excel workbook using `openpyxl`.
- Includes the date for each row of data.

## Requirements

- Python 3.6+
- Chrome browser and ChromeDriver installed
- `chromedriver` executable in your system's PATH or in the same directory as the script

## Installation

1. Clone the repository or download the script.

2. Install the required Python libraries:
   ```bash
   pip install -r requirments.txt
   ```

3. Download the ChromeDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads) and ensure it is executable.

## Usage

To run the script, simply execute:
```bash
python sel_script.py
```

The script will:
- Open the Baseball Monster website using Selenium.
- Iterate over the dates available in the calendar, clicking each date to load the data.
- Scrape the batting and pitching data for each date.
- Save the data to an Excel workbook named `baseball_data_newMarch.xlsx`.

## Script Details

### Functions

- `write_match_data(ws, match_data, headers, date)`: Writes the match data to the specified worksheet in the Excel workbook.

### Web Scraping

- The script uses Selenium to interact with the Baseball Monster website, clicking on calendar dates to load historical data.
- BeautifulSoup is used to parse the HTML content and extract relevant data from the tables.
- The script processes tables in pairs (one for batting and one for pitching) and extracts headers and rows of data.

### Data Processing

- Opponent team and win/loss information are determined using regex matching on the match details.
- The data for each date is stored in an Excel workbook, with separate sheets for batting and pitching data.

### Saving to Excel

- The script uses `openpyxl` to create and manipulate Excel workbooks.
- The date is included in each row to indicate when the match data was recorded.
- The workbook is saved as `baseball_data_newMarch.xlsx`.

## Customization

- **URL**: Change the `url` variable in the script to scrape data from a different page.
- **Excel File Name**: Modify the `wb.save('baseball_data_newMarch.xlsx')` line to change the name of the output Excel file.

## Error Handling

The script includes basic error handling for Selenium operations. If an error occurs, the WebDriver is closed properly.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments

- [Selenium WebDriver](https://www.selenium.dev/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [openpyxl](https://openpyxl.readthedocs.io/en/stable/)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

## Contact

For any inquiries or issues, please contact [pranajlrana1235@gmail.com]