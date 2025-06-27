from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse
from google import genai
from urllib import robotparser
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize the Gemini client
client = genai.Client()

# Toggle to enable or disable robots.txt compliance
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
        logging.warning(f"Couldn't fetch or parse robots.txt: {e}")
        return False

def scrape_web_page(url):
    if not can_scrape(url):
        logging.warning(f"Skipping {url} due to robots.txt restrictions.")
        return []

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        logging.info("Retrieving context...")
        text = soup.get_text()
        return [text]

    except Exception as e:
        logging.error(f"Failed to scrape {url}: {e}")
        return []

def main():
    use_rag = input("Use RAG mode? (yes/no): ").strip().lower() == "yes"
    query = input("Ask something: ")

    if use_rag:
        url = os.getenv("WEB_URL")
        website_texts = scrape_web_page(url)
        if website_texts:
            logging.info("Augmenting context...")
            combined_context = "\n".join(website_texts)[:4000]
            prompt = f"Based on the following content:\n{combined_context}\n\nAnswer the question:\n{query}"
        else:
            logging.warning("No content found. Proceeding with default model prompt.")
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