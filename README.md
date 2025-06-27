# 🦔 DurianBot

**DurianBot**: A spiky little RAG-powered crawler that cracks open websites like durians—tough on the outside, rich in answers on the inside. May smell funky, but the insights are premium.

## 🧠 What It Does

DurianBot is a mini chatbot that combines **Retrieval-Augmented Generation (RAG)** with the **Gemini API (LLM)** to help answer user queries. It scrapes relevant content from a specified website, serves that context to the LLM, and delivers responses that are smarter than your average fruit.

## 🍽️ Features

- Extracts content from only the **first page** of a given website
- **Two modes**:  
  - **RAG-enabled** (LLM + website context)  
  - **LLM-only** (pure model response)
- Uses **Gemini 2.5 Flash** for lightning-fast content generation
- **Robots.txt compliance toggle**: Respect the website's scraping permissions

## 🚀 How to Use

1. Run the script (Windows):
   ```bash
   python -m virtualenv gemini_env
   .\gemini_env\Scripts\activate
   pip install -q -U google-genai requests beautifulsoup4
   set "WEB_URL=https://raw.githubusercontent.com/linkedbing/DurianBot/refs/heads/main/durianbot_healthchat_demo"
   set "GEMINI_API_KEY=your-gemini-api-key"
   python durianbot.py

## 🖼️ Sample Input & Output

**Input:**

Does it hold true that an apple a day keeps the doctor away?

**Output (RAG: ✅ Enabled – Based on [retrieved health data](https://raw.githubusercontent.com/linkedbing/DurianBot/refs/heads/main/durianbot_healthchat_demo)):**

**True**, as daily apple consumption has been linked to fewer non-critical doctor visits and acts as preventive care.

**Output (RAG: ❌ Disabled – No support data):**

**False**, it's a proverb that emphasizes the benefits of healthy eating, not a literal guarantee.


## ⚠️ Disclaimer

- This project is for **educational purposes only**. Always use responsibly and in accordance with website terms of service.
- Scraping may not be permitted on all sites—**use the robot compliance toggle with care and ethical consideration**.
- **You are solely responsible for how you use this tool**. We are not liable for misuse, scraping violations, or generated content.
- Always follow local laws and target site terms of service.
- DurianBot does not guarantee factually accurate, complete, or safe responses from the LLM. Do not use it for legal, medical, or sensitive advice.
- Use of this software implies that **you accept full responsibility** for its ethical and lawful use.

## 📄 License
Licensed under the MIT License. Feel free to fork, remix, and share—just keep it durian-scented 🍃
