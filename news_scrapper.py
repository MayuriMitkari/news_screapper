import requests
from bs4 import BeautifulSoup
import datetime

URL = "https://www.bbc.com/news"
OUTPUT_FILE = "headlines.txt"

def scrape_headlines():
    print("Fetching headlines from BBC News...")

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Try to get headlines from h3 and h2 tags
        headline_tags = soup.find_all(['h3', 'h2'])

        headlines = []
        for tag in headline_tags:
            text = tag.get_text(strip=True)
            if text and len(text) > 15:  # Filter out short non-headline text
                headlines.append(text)

        if not headlines:
            print("No headlines found. The page structure may have changed.")
            return

        save_to_file(headlines)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def save_to_file(headlines):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as file:
        file.write(f"Top Headlines from BBC News\n")
        file.write(f"Scraped on: {timestamp}\n")
        file.write("="*40 + "\n\n")
        for i, title in enumerate(headlines, 1):
            file.write(f"{i}. {title}\n")

    print(f"✅ Success! {len(headlines)} headlines have been scraped and saved to '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    scrape_headlines()
