import time
import psycopg2
from bs4 import BeautifulSoup
import requests

def get_db_connection(max_retries=5, retry_delay=5):
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(
                host="db",
                dbname="sentiment_analysis_db",
                user="user",
                password="password"
            )
            print("✅ Database connection established")
            return conn
        except psycopg2.OperationalError as e:
            print(f"❌ Connection attempt {i+1}/{max_retries} failed: {e}")
            if i < max_retries - 1:
                time.sleep(retry_delay)
    raise RuntimeError("Could not establish database connection")

def scrape_data():
    try:
        url = "https://www.nytimes.com"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return [h.text for h in soup.find_all('h2')]
    except Exception as e:
        print(f"⚠️ Scraping error: {e}")
        return []

def main():
    while True:
        print("\n=== Scraping cycle started ===")
        try:
            # Get data
            headlines = scrape_data()
            print(f"📰 Found {len(headlines)} headlines")
            
            # Store in DB
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scraped_data (
                    id SERIAL PRIMARY KEY,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
            
            for headline in headlines:
                cursor.execute(
                    "INSERT INTO scraped_data (content) VALUES (%s)",
                    (headline,)
                )
            
            conn.commit()
            print(f"💾 Saved {len(headlines)} records")
            
        except Exception as e:
            print(f"🔴 Critical error: {e}")
        finally:
            if 'conn' in locals():
                conn.close()
        
        time.sleep(300)

if __name__ == "__main__":
    main()
