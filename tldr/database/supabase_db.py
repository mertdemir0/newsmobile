from supabase_py import create_client, Client
import os

# Initialize Supabase client using environment variables
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_API_KEY = os.environ.get('SUPABASE_API_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

def fetch_rss_structure() -> dict:
    """
    Fetch the RSS structure from the Supabase table 'rss_feeds'.
    
    Returns:
        dict: A dictionary containing countries as keys, topics as sub-keys, 
              and a list of source names and URLs as values.
    
    Raises:
        Exception: If there's an error fetching data from the database.
    """
    try:
        result = supabase.table('rss_feeds').select().execute()
        data = result.data
        
        # Data transformation logic
        rss_structure = {}
        for item in data:
            country = item['country']
            topic = item['topic']
            source_name = item['source_name']
            source_url = item['source_url']

            if country not in rss_structure:
                rss_structure[country] = {}
            if topic not in rss_structure[country]:
                rss_structure[country][topic] = []

            rss_structure[country][topic].append({
                'name': source_name,
                'url': source_url
            })
        
        return rss_structure
        
    except Exception as e:
        print(f"Error fetching RSS structure: {e}")
        raise
