

# Politics Article Scraper and Sentiment Analysis

This project scrapes articles from the "Politics" section of the myRepublica website, analyzes their sentiment, and extracts names from the article titles and content. The results are saved to a CSV file for further analysis.

## Features

- Scrapes titles, publication dates, and content from politics articles.
- Analyzes sentiment using Google Cloud's Natural Language API.
- Extracts last names and full names from article titles and content.
- Saves results to a CSV file.

## Important Note

In the political landscape, politicians often act as standalone figures and may frequently change parties. As a result, the sentiment expressed in articles might be directed more towards the individual rather than their respective party affiliations.

## Limitations 

The script assumes that the article title has some last name in it which it uses to find the primary political entity in the article content. Without this, we cannot deduce the primary entity in the article and therefore cannot extract the corresponding name. 

## Requirements

- Python 3.7 or higher
- Libraries:
  - `requests`
  - `beautifulsoup4`
  - `pandas`
  - `google-cloud-language`
  - `spacy`
  - `urllib3`
- Google Cloud credentials for the Natural Language API.

## Setup

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install required packages:**

   You can install the required packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Cloud credentials:**

   - Create a service account in the Google Cloud Console and download the JSON key file.
   - Place the JSON file in the project directory and update the `credentials_path` variable in the code.

## Usage

1. **Run the script:**

   Make sure the script file is named `main.py` (or any name you prefer), and then run it:

   ```bash
   python main.py
   ```

2. **Output:**

   The script will scrape the articles and save the results to a CSV file named `myrepublica_politics_articles.csv`. The CSV file will contain the following columns:
   - Title
   - Link
   - Date
   - Content
   - Last_Name
   - Full_Name
   - Sentiment


## Acknowledgments

- Thanks to [myRepublica](https://myrepublica.nagariknetwork.com) for providing the articles.
- Thanks to [Google Cloud](https://cloud.google.com/natural-language/docs) for their Natural Language API.
- Thanks to [spaCy](https://spacy.io) for their powerful NLP library.



