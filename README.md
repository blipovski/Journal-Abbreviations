# Academic Journal Abbreviation Database

This Python script converts HTML data from multiple URLs containing journal titles and their respective abbreviations into an SQLite database. The script fetches data from specified URLs, processes the HTML content, and stores the extracted journal titles and abbreviations in an SQLite database, facilitating easy access and management of journal information.

## Features

- **Data Extraction:** The script utilizes BeautifulSoup to parse HTML content, extracting journal titles and their corresponding abbreviations from specified URLs.
- **Data Cleaning:** It cleans and processes the extracted data, ensuring uniformity and consistency in the stored information.
- **SQLite Integration:** The script seamlessly integrates with SQLite, providing a lightweight and efficient database solution for storing journal data.
- **Custom Capitalization Logic:** It applies custom capitalization logic to ensure proper capitalization of journal titles, handling exceptions like "of" and "the" to maintain title case format.

## Requirements

- Python 3.x
- BeautifulSoup4
- requests

## Installation

Clone the repository:

```bash
git clone https://github.com/blipovski/html-to-sqlite-converter.git
```

Install the required Python packages:

```bash
pip install beautifulsoup4 requests
```

## Usage

Modify the main function in the converter.py script to adjust the URLs, database name, and other parameters as needed.

Run the script:

```bash
python html-sql.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
