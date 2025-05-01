import time
import psycopg2
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

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

def analyze_sentiment(text):
    return analyzer.polarity_scores(text)['compound']

def main():
    while True:
        print("\n=== Analysis cycle started ===")
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Create analysis table if not exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analyzed_data (
                    id SERIAL PRIMARY KEY,
                    scraped_id INTEGER REFERENCES scraped_data(id),
                    sentiment_score FLOAT,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
            
            # Get unprocessed data
            cursor.execute("""
                SELECT id, content FROM scraped_data
                WHERE NOT EXISTS (
                    SELECT 1 FROM analyzed_data 
                    WHERE analyzed_data.scraped_id = scraped_data.id
                )
                LIMIT 100
            """)
            
            records = cursor.fetchall()
            print(f"🔍 Found {len(records)} unprocessed records")
            
            # Analyze and store
            for record_id, content in records:
                score = analyze_sentiment(content)
                cursor.execute("""
                    INSERT INTO analyzed_data
                    (scraped_id, sentiment_score)
                    VALUES (%s, %s)
                """, (record_id, score))
            
            conn.commit()
            print(f"📊 Analyzed {len(records)} records")
            
        except Exception as e:
            print(f"🔴 Critical error: {e}")
        finally:
            if 'conn' in locals():
                conn.close()
        
        time.sleep(60)

if __name__ == "__main__":
    main()
