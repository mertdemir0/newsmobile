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
# ----------------------------- Full Text Extraction -----------------------------
def get_full_text(url):
    try:
        article = Article(url)
        return article.text
    except Exception as e:
        print(f"An error occurred while fetching full text: {e}")
        return None
# ----------------------------- Text Summarizer -----------------------------
class TextSummarizer:
    def __init__(self, model_name="facebook/bart-large-cnn"):
        pass
    def summarize(self, text, max_input_length=1024, max_output_length=150):
        inputs = self.tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=max_input_length, truncation=True)
        summary_ids = self.model.generate(inputs, max_length=max_output_length, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
        return self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
# ----------------------------- RSS Feed -----------------------------
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
        # To display the content
        for article in all_articles:
            print(f"Topic: {article['topic']}")
            print(f"Title: {article['title']}")
        print(f"Summary: {article['summary']}")
        print("-" * 50)
# Move credentials to a secure location
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/secure/credentials.json"
    # Fetch articles asynchronously
def fetch_articles_async(country, topic, language):
    import concurrent.futures
    import asyncio

    # Fetch articles asynchronously
    with concurrent.futures.ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        tasks = [loop.run_in_executor(executor, fetch_article, rss_link, language) for rss_link in rss_feeds.get(country, {}).get(topic, [])]
    return tasks
    articles_list = []
    for article in articles:
        article_dict = {
            'title': article['title'],
            'summary': article['summary']
    }
    articles_list.append(article_dict)
def fetch_article(rss_link, language):
    # Validate and sanitize the input URL
    if not rss_link.startswith("https://"):
        raise ValueError("Invalid URL")
        summary = summarize_text(article.text, language)
def summarize_text(text):
    """Generates a summary of the text using BERT."""
    return model(text)
    # Disable debug mode in production
    app.run(debug=False)
# ----------------------------- Flask App --------------------------------
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
    summary = summarizer.summarize(text)
    return jsonify(summary)
@app.route("/rss", methods=["POST"])
def get_rss_feed():
    country = data["country"]
    topic = data["topic"]
    url = rss_feeds[country][topic]
    return jsonify(articles)