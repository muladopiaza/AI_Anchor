import requests
import random
import os
from scraper import get_articles  # Assuming your scraper already works

# --- Config ---
api_key = os.getenv('HF_API_KEY')
API_KEY = api_key
API_URL = "https://api-inference.huggingface.co/models/gpt2"  # Testing with GPT-2 model

# --- Random Anchor Name ---
def get_random_anchor_name():
    first_names = ['David', 'Sarah', 'James', 'Emily', 'Michael', 'Emma', 'Daniel', 'Sophia', 'John', 'Olivia']
    last_names = ['Smith', 'Johnson', 'Brown', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin']
    return f"{random.choice(first_names)} {random.choice(last_names)}"

# --- Query LLM ---
def query_llm(payload):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        print(f"Error from API: {response.status_code}, {response.text}")
        return None
    
    output = response.json()

    if isinstance(output, list) and len(output) > 0 and 'generated_text' in output[0]:
        return output[0]['generated_text']
    else:
        print("Unexpected output format:", output)
        return None

# --- Token Length Check ---
def count_tokens(text):
    return len(text.split())  # Simple token counting by word

# --- Process News ---
def process_news(text):
    anchor_name = get_random_anchor_name()

    # Trim the text to fit within token limits
    input_tokens = count_tokens(text)
    if input_tokens > 300:
        text = " ".join(text.split()[:300])  # Truncate to 300 tokens for better balance

    prompt = f"Hello, I'm {anchor_name}. Here's today's top stories:\n\n{text}\n\nThat's the latest news, thank you for watching."

    output_text = query_llm({
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 300,
            "temperature": 0.6
        }
    })

    if output_text:
        return output_text.strip()

    return text  # fallback

# --- MAIN ---
if __name__ == "__main__":
    news_site_url = 'https://www.bbc.com/'  # You can change if needed
    articles = get_articles(news_site_url, max_articles=20)  # Get news
    raw_news = '\n\n'.join(articles)  # Join all articles

    anchor_script = process_news(raw_news)

    print(anchor_script)
