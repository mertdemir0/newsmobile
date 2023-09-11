import feedparser
from models.text_summarizer import TextSummarizer
from utils.article_processing import get_full_text

def parse_rss_and_fetch_content(url, topic):
    try:
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
    except Exception as e:
        # In a real-world scenario, this would be logged using a logger.
        return {"success": False, "error": str(e)}