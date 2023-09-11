from newspaper import Article

def get_full_text(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        # Instead of print, in a real-world scenario, a logger can be used.
        print(f"An error occurred while fetching full text: {e}")
        return None