import requests
from bs4 import BeautifulSoup
import sqlite3
from tqdm import tqdm

# Function to fetch journal data from a single URL
def fetch_journal_data(url):
    print(f"Fetching data from {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    journal_data = []

    # Find the <dl> tag
    dl_tag = soup.find('dl')

    if dl_tag:
        # Extract journal titles and abbreviations from <dt> and <dd> tags
        dt_tags = dl_tag.find_all('dt')
        dd_tags = dl_tag.find_all('dd')

        # Iterate over <dt> and <dd> pairs to extract data
        for dt, dd in zip(dt_tags, dd_tags):
            # Split the text by newlines
            title_lines = dt.get_text().strip().split('\n')
            abbreviation_lines = dd.get_text().strip().split('\n')

            # Iterate through the lines to process each one
            for title_line, abbreviation_line in zip(title_lines, abbreviation_lines):
                # Capitalize journal titles using custom logic
                words = title_line.strip().split()
                title = ' '.join(word.capitalize() if i == 0 or word.lower() not in ['of', 'and', 'on', 'in', 'the', 'for'] else word.lower() for i, word in enumerate(words))
                # Capitalize each word's first letter for journal abbreviations
                abbreviation = ' '.join(word.capitalize() for word in abbreviation_line.strip().split())
                journal_data.append((title, abbreviation))

    return journal_data

# Function to create SQLite database and table
def create_sqlite_db(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS journals
                      (title TEXT, abbreviation TEXT)''')
    conn.commit()
    conn.close()

# Function to insert data into SQLite database
def insert_data_into_db(db_name, data):
    print(f"Inserting data into DB: {data}")
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO journals (title, abbreviation) VALUES (?, ?)", data)
    conn.commit()
    conn.close()
    print("Data insertion successful")

# Main function to orchestrate the process
def main():
    # URLs for journal data
    base_url = "https://images.webofknowledge.com/images/help/WOS/"
    urls = [base_url + "0-9_abrvjt.html"] + \
           [base_url + char + "_abrvjt.html" for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]

    # Database name
    db_name = 'journals.db'

    # Create SQLite database and table
    create_sqlite_db(db_name)

    # Initialize tqdm with the total number of URLs to process
    progress_bar = tqdm(urls, desc="Processing URLs", unit="URL")

    # Fetch data from each URL and insert into the database
    for url in progress_bar:
        try:
            journal_data = fetch_journal_data(url)
            insert_data_into_db(db_name, journal_data)
            progress_bar.set_postfix({"URL": url[-15:]})  # Update progress bar description with the current URL
        except Exception as e:
            print(f"Error occurred while processing {url}: {str(e)}")

    print("All data inserted successfully!")

if __name__ == "__main__":
    main()