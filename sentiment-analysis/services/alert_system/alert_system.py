import time
import psycopg2
import redis
from flask import Flask
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

# --- CORS CONFIGURATION ---
# Allow only your frontend origin in production. 
# For development, you may use origins="*" (all origins).
CORS(
    app,
    resources={r"/alerts": {"origins": [
        "http://localhost:3000",              # Local development
        "http://ap7.humanbrain.in:3000"       # Your deployed frontend
    ]}},
    supports_credentials=True                # Allow credentials if you use cookies/auth
)
# --------------------------

r = redis.Redis(host='redis', port=6379, db=0)

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

def check_alerts():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM analyzed_data
            WHERE (sentiment_score < -0.8 OR sentiment_score > 0.8)
            AND created_at > NOW() - INTERVAL '5 minutes'
        """)
        alert_count = cursor.fetchone()[0]
        r.set('alert_count', alert_count)
        print(f"🚨 Active alerts: {alert_count}")
    except Exception as e:
        print(f"⚠️ Alert check failed: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def alert_loop():
    while True:
        check_alerts()
        time.sleep(10)

@app.route('/alerts')
def get_alerts():
    try:
        count = int(r.get('alert_count') or 0)
        return {'alerts': count, 'status': 'success'}
    except Exception as e:
        return {'error': str(e), 'status': 'failed'}, 500

if __name__ == "__main__":
    import threading
    threading.Thread(target=alert_loop, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
