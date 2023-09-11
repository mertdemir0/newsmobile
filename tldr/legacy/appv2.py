from flask import Flask, jsonify, request
import os
from google.cloud import translate_v2 as translate
import feedparser
from newspaper import Article
from summarizer import Summarizer

app = Flask(__name__)

# Google Translate and Summarizer setup
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"
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

    # Iterate over all links for the given country and topic
    for rss_link in rss_feeds.get(country, {}).get(topic, []):
        feed = feedparser.parse(rss_link)
        for entry in feed.entries:
            article = Article(entry.link)
            article.download()
            article.parse()

            title = translate_text(article.title, language)
            summary = summarize_text(article.text)  # Use BERT summarizer
            summary = translate_text(summary, language)  # Then translate

            articles_list.append({
                'title': title,
                'summary': summary
            })

    return jsonify(articles_list)

def translate_text(text, target_language):
    """Translates text into the target language."""
    if not text:
        return ""

    translation = translate_client.translate(text, target_language=target_language)
    return translation['translatedText']

def summarize_text(text):
    """Generates a summary of the text using BERT."""
    return model(text)

if __name__ == '__main__':
    app.run(debug=True)