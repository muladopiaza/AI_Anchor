import time
from newspaper import Article, build
from concurrent.futures import ThreadPoolExecutor, as_completed

IMPORTANT_KEYWORDS = [
    'war', 'conflict', 'government', 'politics', 'finance', 'economy',
    'election', 'trade', 'parliament', 'policy', 'military', 'terror',
    'inflation', 'diplomacy', 'strike', 'sanctions', 'peace talks', 'summit',
    'president', 'prime minister', 'budget', 'UN', 'crisis', 'security',
]

WORD_LIMIT = 300  # Limit the number of words per article

def is_important(text):
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in IMPORTANT_KEYWORDS)

def limit_words(text, word_limit):
    """Function to limit the number of words in a text."""
    words = text.split()
    return ' '.join(words[:word_limit])  # Join the first `word_limit` words

def scrape_article(content):
    try:
        article = Article(content.url)
        article.download()
        article.parse()

        if not article.text.strip():
            return None

        # Limit the number of words in the article
        limited_text = limit_words(article.text, WORD_LIMIT)

        if is_important(article.title) or is_important(article.text):
            return limited_text
        else:
            return None

    except Exception as e:
        return None

def fetch_frontpage_articles(news_site_url, max_articles=20, num_workers=10):
    paper = build(news_site_url, memoize_articles=False)
    articles = []
    contents = paper.articles[:max_articles]  # Limit to top 20 articles

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_article = {executor.submit(scrape_article, content): content for content in contents}
        for future in as_completed(future_to_article):
            result = future.result()
            if result:
                articles.append(result)

    return articles

def print_articles(articles):
    # Print only the text of the important articles
    for article in articles:
        print(article)  # Print the full text of the important article

def get_articles(news_site_url, max_articles=20):
    """
    Function to return articles without printing them, for use in other scripts or functions.
    """
    articles = fetch_frontpage_articles(news_site_url, max_articles)
    return articles

# Example usage
if __name__ == "__main__":
    news_site_url = 'https://www.bbc.com/'  # You can change this to any other site you prefer
    articles = fetch_frontpage_articles(news_site_url, max_articles=20, num_workers=10)
    
    # Print only the full article texts
    print_articles(articles)
