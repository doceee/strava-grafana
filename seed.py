import os
import mysql.connector
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
REFRESH_TOKEN = os.getenv('STRAVA_REFRESH_TOKEN')
TOKEN_URL = "https://www.strava.com/oauth/token"

MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

DB_CONFIG = {
    'host': MYSQL_HOST,
    'port': MYSQL_PORT,
    'user': MYSQL_USER,
    'password': MYSQL_PASSWORD,
    'database': MYSQL_DATABASE
}

def get_access_token():
    url = TOKEN_URL
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN
    }

    response = requests.post(url, data=payload)

    return response.json()["access_token"]

def fetch_activities(access_token, per_page=50):
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"per_page": per_page, "page": 1}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def save_to_mysql(data):
    cnx = mysql.connector.connect(**DB_CONFIG)
    cursor = cnx.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS strava_activities (
            id BIGINT PRIMARY KEY,
            name TEXT,
            distance FLOAT,
            moving_time INT,
            elapsed_time INT,
            total_elevation_gain FLOAT,
            type TEXT,
            start_date TIMESTAMP
        );
    """)

    for activity in data:
        cursor.execute("""
            INSERT IGNORE INTO strava_activities (id, name, distance, moving_time, elapsed_time,
                                                  total_elevation_gain, type, start_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            activity['id'],
            activity['name'],
            activity['distance'],
            activity['moving_time'],
            activity['elapsed_time'],
            activity['total_elevation_gain'],
            activity['type'],
            datetime.strptime(activity['start_date'], '%Y-%m-%dT%H:%M:%SZ')
        ))

    cnx.commit()
    cursor.close()
    cnx.close()

if __name__ == "__main__":
    token = get_access_token()
    activities = fetch_activities(token)
    save_to_mysql(activities)
    print(f"Imported {len(activities)} activities.")
