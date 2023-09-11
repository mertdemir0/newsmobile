import asyncio
import concurrent.futures
from flask import Flask, jsonify, request
import os
from google.cloud import translate_v2 as translate
import feedparser
from newspaper import Article
from summarizer import Summarizer

app = Flask(__name__)

# Google Translate and Summarizer setup
# Move credentials to a secure location
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/secure/credentials.json"
translate_client = translate.Client()
model = Summarizer()

rss_feeds = {
    "USA": {
        "technology": "https://usa-tech.example.com/rss_feed.xml",
        "sports": "https://usa-sports.example.com/rss_feed.xml",
        "health": "https://usa-health.example.com/rss_feed.xml",
    },
    "UK": {
        "technology": "https://uk-tech.example.com/rss_feed.xml",
        "sports": "https://uk-sports.example.com/rss_feed.xml",
        "health": "https://uk-health.example.com/rss_feed.xml",
    },
    # Add more countries and topics as needed
}

@app.route('/get_rss_structure', methods=['GET'])
def get_rss_structure():
    return jsonify(rss_feeds)

@app.route('/get_articles', methods=['GET'])
def get_articles():
    country = request.args.get('country')
    topic = request.args.get('topic')
    language = request.args.get('language', 'en')

    articles_list = []

    # Fetch articles asynchronously
    with concurrent.futures.ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        tasks = [loop.run_in_executor(executor, fetch_article, rss_link, language) for rss_link in rss_feeds.get(country, {}).get(topic, [])]
        articles = loop.run_until_complete(asyncio.gather(*tasks))

    for article in articles:
        articles_list.append({
            'title': article['title'],
            'summary': article['summary']
        })

    return jsonify(articles_list)

def fetch_article(rss_link, language):
    # Validate and sanitize the input URL
    if not rss_link.startswith("https://"):
        raise ValueError("Invalid URL")

    feed = feedparser.parse(rss_link)
    articles = []

    for entry in feed.entries:
        article = Article(entry.link)
        article.download()
        article.parse()

        title = translate_text(article.title, language)
        summary = summarize_text(article.text, language)

        articles.append({
            'title': title,
            'summary': summary
        })

    return articles

def translate_text(text, target_language):
    """Translates text into the target language."""
    if not text:
        return ""

    translation = translate_client.translate(text, target_language=target_language)
    return translation['translatedText']

def summarize_text(text, language):
    """Generates a summary of the text using a summarization model."""
    # Validate and sanitize the input text
    if not text:
        return ""

    # Use a lighter and faster summarization model instead of BERT
    return model(text, language)

if __name__ == '__main__':
    # Disable debug mode in production
    app.run(debug=False)