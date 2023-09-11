import concurrent.futures
import asyncio
from utils.article_processing import get_full_text
from utils.text_processing import summarize_text

def fetch_articles_async(country, topic, language, rss_feeds):
    articles = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        tasks = [loop.run_in_executor(executor, fetch_article, rss_link, language) for rss_link in rss_feeds.get(country, {}).get(topic, [])]
        for response in asyncio.as_completed(tasks):
            articles.append(response.result())
    return articles

def fetch_article(rss_link, language):
    if not rss_link.startswith("https://"):
        raise ValueError("Invalid URL")
    article_text = get_full_text(rss_link)
    summary = summarize_text(article_text)
    return summary