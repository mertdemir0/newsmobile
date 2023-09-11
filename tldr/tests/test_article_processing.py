import pytest
from utils.article_processing import get_full_text

def test_article_fetching():
    article_url = "SAMPLE_ARTICLE_URL"  # Replace with an actual article URL for testing.
    content = get_full_text(article_url)
    
    assert isinstance(content, str)
    assert len(content) > 0