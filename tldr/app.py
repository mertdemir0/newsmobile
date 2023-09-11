from flask import Flask, request, jsonify
from services.rss_service import fetch_articles_async
from utils.article_processing import get_full_text
import feedparser

app = Flask(__name__)

@app.route('/get_rss_structure', methods=['GET'])
def get_rss_structure():
    try:
        # Placeholder for the function where you fetch the RSS structure.
        # Fetch from database or other source
        rss_structure = {} 
        return jsonify({"success": True, "data": rss_structure})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/get_articles', methods=['GET'])
def get_articles():
    try:
        country = request.args.get('country')
        topic = request.args.get('topic')
        language = request.args.get('lang')
        
        # Use the fetch_articles_async function to get articles
        articles = fetch_articles_async(country, topic, language)
        return jsonify({"success": True, "data": articles})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/rss', methods=['GET'])
def get_rss_articles():
    try:
        country = request.args.get('country')
        topic = request.args.get('topic')
        
        # Placeholder for fetching the RSS URL from your database or other source
        rss_url = {}
        feed = feedparser.parse(rss_url.get(country, {}).get(topic, ""))
        
        articles = []
        for entry in feed.entries:
            article_content = get_full_text(entry.link)
            articles.append({
                'title': entry.title,
                'description': entry.description,
                'link': entry.link,
                'published': entry.published,
                'content': article_content
            })
        
        return jsonify({"success": True, "data": articles})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)