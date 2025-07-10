# 🦔 DurianBot

**DurianBot**: A spiky little context-engineering crawler that cracks open websites like durians—tough on the outside, rich in answers on the inside. May smell funky, but the insights are premium.

## 🧠 What It Does

DurianBot is a mini chatbot that applies **Context Engineering techniques** in combination with the **Gemini API (LLM)** to answer user queries intelligently. It scrapes relevant content from a specified website, filters and compresses it based on the query, injects curated context into the model, and delivers responses that are smarter than your average fruit.

## 🍽️ Features

- Extracts content from only the **first page** of a given website  
- **Two modes**:  
  - **Context Engineering Enabled** (Query-aware filtering + summarization + Gemini response)  
  - **LLM-only** (pure model response without external context)  
- Uses **Gemini 2.5 Flash** for lightning-fast content generation  
- Employs **semantic relevance filtering**, **context summarization**, and **multi-turn memory**  
- **Robots.txt compliance toggle**: Respect the website's scraping permissions

## 🚀 How to Use

1. Run the script (Windows):

   ```bash
   python -m virtualenv gemini_env
   .\gemini_env\Scripts\activate
   pip install -q -U google-genai requests beautifulsoup4 sentence-transformers
   set "WEB_URL=https://raw.githubusercontent.com/linkedbing/DurianBot/refs/heads/main/dummy-durian-health-study.md"
   set "GEMINI_API_KEY=your-gemini-api-key"
   python durianbot.py

## 🖼️ Sample Input & Output

**Input:**
```bash
Does it hold true that a durian a day keeps the doctor away?
```

**Output (Context Engineering: ✅ Enabled – Advanced AI + Referenced [dummy health study](https://github.com/linkedbing/DurianBot/blob/main/dummy-durian-health-study.md)):**
```bash
Based on the provided curated context:

A "whimsical investigation" **suggests** daily durian consumption "may reduce doctor visits." However, the context **humorously attributes** this to the fruit's potent odor deterring close contact, rather than a direct health benefit.

Therefore, while the context *suggests* it in a lighthearted way, it does not present "a durian a day keeps the doctor away" as a definitively proven medical fact.
```
**Output (Context Engineering: ❌ Disabled – Standard AI):**
```bash
No, the statement is not medically verified.

The phrase is a humorous variation of the proverb "An apple a day keeps the doctor away," 
used to encourage healthy eating habits. It is not intended as literal medical advice.
```

## ⚠️ Disclaimer

- This project is for **educational purposes only**. Always use responsibly and in accordance with website terms of service.
- Scraping may not be permitted on all sites—**use the robot compliance toggle with care and ethical consideration**.
- **You are solely responsible for how you use this tool**. We are not liable for misuse, scraping violations, or generated content.
- Always follow local laws and target site terms of service.
- DurianBot does not guarantee factually accurate, complete, or safe responses from the LLM. Do not use it for legal, medical, or sensitive advice.
- Use of this software implies that **you accept full responsibility** for its ethical and lawful use.

## 📄 License
Licensed under the MIT License. Feel free to fork, remix, and share—just keep it durian-scented 🍃
