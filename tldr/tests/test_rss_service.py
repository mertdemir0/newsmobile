import pytest
from services.rss_service import parse_rss_and_fetch_content

def test_rss_parsing():
    rss_url = "SAMPLE_RSS_URL"  # Replace with an actual RSS URL for testing.
    topic = "general"
    articles = parse_rss_and_fetch_content(rss_url, topic)
    
    assert isinstance(articles, list)
    assert len(articles) > 0
    assert 'title' in articles[0]
    assert 'description' in articles[0]
    assert 'link' in articles[0]