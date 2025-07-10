from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
from google import genai
from urllib import robotparser
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize the Gemini client
client = genai.Client()
ENABLE_ROBOTS_CHECK = True

def can_scrape(url):
    if not ENABLE_ROBOTS_CHECK:
        return True
    parsed_url = urlparse(url)
    robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
    rp = robotparser.RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
        return rp.can_fetch("*", url)
    except Exception as e:
        logging.warning(f"Couldn't parse robots.txt: {e}")
        return False

def scrape_web_page(url):
    if not can_scrape(url):
        logging.warning(f"Skipping {url} due to robots.txt.")
        return ""

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        logging.info("Retrieved full content.")
        return text
    except Exception as e:
        logging.error(f"Scraping failed: {e}")
        return ""

def summarize_context(text):
    logging.info("Summarizing context...")
    prompt = f"Summarize this content concisely:\n{text[:3500]}"
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text.strip()

def main():
    use_context_engineering = input("Use Context Engineering mode? (yes/no): ").strip().lower() == "yes"
    query = input("Ask something: ")

    if use_context_engineering:
        url = os.getenv("WEB_URL")
        raw_text = scrape_web_page(url)
        if raw_text:
            summarized = summarize_context(raw_text)
            logging.info("Injecting compressed context...")
            prompt = f"Using the following context:\n{summarized}\n\nAnswer this:\n{query}"
        else:
            logging.warning("No content found. Proceeding without context.")
            prompt = query
    else:
        prompt = query

    logging.info("Generating response...")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    print("\nResponse:\n" + response.text)

if __name__ == "__main__":
    main()
