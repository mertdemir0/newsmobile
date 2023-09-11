import feedparser
from newspaper import Article
from transformers import BartTokenizer, BartForConditionalGeneration
from flask import Flask, jsonify, request
import os
from google.cloud import translate_v2 as translate
from summarizer import Summarizer

# ----------------------------- Full Text Extraction -----------------------------

def get_full_text(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"An error occurred while fetching full text: {e}")
        return None
    
# ----------------------------- Text Summarizer -----------------------------
class TextSummarizer:
    def __init__(self, model_name="facebook/bart-large-cnn"):
        self.tokenizer = BartTokenizer.from_pretrained(model_name)
        self.model = BartForConditionalGeneration.from_pretrained(model_name)

    def summarize(self, text, max_input_length=1024, max_output_length=150):
        inputs = self.tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=max_input_length, truncation=True)
        summary_ids = self.model.generate(inputs, max_length=max_output_length, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
        return self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    
# ----------------------------- RSS Feed -----------------------------
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
    
# ----------------------------- Flask App --------------------------------
app = Flask(__name__)

@app.route("/translate", methods=["POST"])
def translate_text():
    data = request.get_json()
    text = data["text"]
    target_language = data["target_language"]
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return jsonify(result)
    
@app.route("/summarize", methods=["POST"])
def summarize_text():
    data = request.get_json()
    text = data["text"]
    summarizer = TextSummarizer()
    summary = summarizer.summarize(text)
    return jsonify(summary)
    
@app.route("/rss", methods=["POST"])
def get_rss_feed():
    data = request.get_json()
    country = data["country"]
    topic = data["topic"]
    url = rss_feeds[country][topic]
    summarizer = TextSummarizer()
    data = feedparser.parse(url)
    articles = []

    for entry in data.entries:
        full_text = get_full_text(entry.link)
        summary = summarizer.summarize(full_text) if full_text else None

        articles.append({
            'title': entry.title,
            'description': entry.description,
            'link': entry.link,
            'publish_date': entry.published,
            'full_text': full_text,
            'summary': summary,
            'topic': topic  # Assigning the topic to each article
        })

    return jsonify(articles)

# ----------------------------- RSS Parsing and Processing -----------------------------
def parse_rss_and_fetch_content(url, topic):
    summarizer = TextSummarizer()
    data = feedparser.parse(url)
    articles = []

    for entry in data.entries:
        full_text = get_full_text(entry.link)
        summary = summarizer.summarize(full_text) if full_text else None

        articles.append({
            'title': entry.title,
            'description': entry.description,
            'link': entry.link,
            'publish_date': entry.published,
            'full_text': full_text,
            'summary': summary,
            'topic': topic  # Assigning the topic to each article
        })

    return articles

# ----------------------------- Testing -----------------------------
if __name__ == "__main__":
    all_articles = []
    
    for topic, rss_link in rss_feeds.items():
        articles_from_feed = parse_rss_and_fetch_content(rss_link, topic)
        all_articles.extend(articles_from_feed)

    # To display the content
    for article in all_articles:
        print(f"Topic: {article['topic']}")
        print(f"Title: {article['title']}")
        print(f"Summary: {article['summary']}")
        print("-" * 50)