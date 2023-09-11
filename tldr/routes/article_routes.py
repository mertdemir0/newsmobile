from flask import jsonify, request
from services.async_article_service import fetch_articles_async
from database.firebase_db import save_article_for_user
from app import app

@app.route('/get_articles', methods=['GET'])
def get_articles_endpoint():
    try:
        country = request.args.get('country')
        topic = request.args.get('topic')
        language = request.args.get('lang')
        articles = fetch_articles_async(country, topic, language)
        return jsonify({"success": True, "data": articles})
    except Exception as e:
        # In a real-world scenario, this would be logged using a logger.
        return jsonify({"success": False, "error": str(e)})

@app.route('/save_article', methods=['POST'])
def save_article_endpoint():
    try:
        user_id = request.json.get('user_id')
        article_data = request.json.get('article')
        success = save_article_for_user(user_id, article_data)
        return jsonify({"success": success})
    except Exception as e:
        # In a real-world scenario, this would be logged using a logger.
        return jsonify({"success": False, "error": str(e)})