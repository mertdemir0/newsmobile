import pytest
from models.text_summarizer import TextSummarizer

def test_summarization():
    summarizer = TextSummarizer()
    text = "OpenAI is an organization that focuses on creating and promoting friendly AI for the benefit of all humanity."
    summary = summarizer.summarize(text)
    
    # Basic checks to ensure summarization works
    assert isinstance(summary, str)
    assert len(summary) < len(text)
    assert "OpenAI" in summary  # Assuming OpenAI would be mentioned in the summary

# Additional tests can be added based on specific requirements and edge cases.
