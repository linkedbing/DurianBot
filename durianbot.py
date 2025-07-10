from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
from google import genai
from urllib import robotparser
import logging
import os
from sentence_transformers import SentenceTransformer, util

# --- Setup ---
logging.basicConfig(level=logging.INFO)
client = genai.Client()
embedder = SentenceTransformer("all-MiniLM-L6-v2")

ENABLE_ROBOTS_CHECK = True
context_memory = []  # Persistent memory across turns

# --- Function: Check robots.txt ---
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

# --- Function: Scrape Web Page ---
def scrape_web_page(url):
    if not can_scrape(url):
        logging.warning(f"Skipping {url} due to robots.txt.")
        return ""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator="\n", strip=True)
        logging.info("Web content retrieved.")
        return text
    except Exception as e:
        logging.error(f"Scraping failed: {e}")
        return ""

# --- Function: Semantic Filtering ---
def filter_relevant_chunks(text, query, top_k=3):
    logging.info("Filtering relevant chunks based on semantic similarity...")
    chunks = [chunk.strip() for chunk in text.split('\n') if len(chunk.strip()) > 100]
    logging.info(f"Total chunks extracted: {len(chunks)}")

    if not chunks:
        logging.warning("No suitable chunks found for filtering.")
        return []
    top_k = min(top_k, len(chunks))
    chunk_embeddings = embedder.encode(chunks, convert_to_tensor=True)
    query_embedding = embedder.encode(query, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(query_embedding, chunk_embeddings)[0]
    top_indices = scores.topk(top_k).indices.tolist()

    relevant_chunks = [chunks[i] for i in top_indices]
    for i, idx in enumerate(top_indices):
        logging.info(f"[{i+1}] Selected Chunk (Score: {scores[idx]:.2f}):\n{chunks[idx][:200]}...\n")

    return relevant_chunks

# --- Function: Summarization ---
def summarize_context(text):
    logging.info("Summarizing context...")
    prompt = f"Summarize this content concisely:\n{text[:3500]}"
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    summary = response.text.strip()
    logging.info(f"Summary preview:\n{summary[:300]}...\n")
    return summary

# --- Function: Memory Update ---
def update_context_memory(new_context):
    logging.info("Updating context memory with new summarized chunk...")
    logging.info(f"New context snippet:\n{new_context[:300]}...\n")
    context_memory.append(new_context)
    if len(context_memory) > 5:
        removed = context_memory.pop(0)
        logging.info(f"Memory limit reached. Oldest context removed:\n{removed[:150]}...\n")
    logging.info(f"Total memory size: {len(context_memory)} entries.")

# --- Function: Combine Context ---
def get_combined_context():
    combined = "\n---\n".join(context_memory)
    logging.info("Final context injected into prompt:")
    logging.info(f"\n{combined[:1000]}...\n")
    return combined

# --- Main Program ---
def main():
    use_context_engineering = input("Use Context Engineering mode? (yes/no): ").strip().lower() == "yes"
    query = input("Ask something: ")
    prompt = query

    if use_context_engineering:
        url = os.getenv("WEB_URL")
        raw_text = scrape_web_page(url)
        if raw_text:
            relevant_chunks = filter_relevant_chunks(raw_text, query)
            compressed_context = summarize_context("\n".join(relevant_chunks))
            update_context_memory(compressed_context)
            final_context = get_combined_context()
            prompt = f"Using the following curated context:\n{final_context}\n\nAnswer this:\n{query}"
        else:
            logging.warning("No content found. Proceeding without context.")

    logging.info("Generating response...")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    print("\nResponse:\n" + response.text)

if __name__ == "__main__":
    main()
