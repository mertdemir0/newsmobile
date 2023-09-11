from flask import jsonify
from database.supabase_db import fetch_rss_structure
from app import app

@app.route('/get_rss_structure', methods=['GET'])
def get_rss_structure_endpoint():
    try:
        rss_data = fetch_rss_structure()
        return jsonify({"success": True, "data": rss_data})
    except Exception as e:
        # In a real-world scenario, this would be logged using a logger for better monitoring.
        return jsonify({"success": False, "error": str(e)})