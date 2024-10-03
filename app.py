from flask import Flask, jsonify
import requests
from collections import defaultdict
from datetime import datetime, timedelta

app = Flask(__name__)

def get_codeforces_submissions(handle):
    url = f"https://codeforces.com/api/user.status?handle={handle}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('result', [])
    return []

def generate_calendar_data(handle):
    submissions = get_codeforces_submissions(handle)
    calendar_data = defaultdict(int)
    
    for submission in submissions:
        if submission.get('verdict') == 'OK':  # Filter only Accepted submissions
            timestamp = submission['creationTimeSeconds']
            date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')
            calendar_data[date] += 1
    
    today = datetime.utcnow()
    start_date = today - timedelta(days=365)
    
    # Fill in all days within the last year, even those with 0 AC submissions
    for day in range(366):  # Cover leap years too
        date_str = (start_date + timedelta(days=day)).strftime('%Y-%m-%d')
        if date_str not in calendar_data:
            calendar_data[date_str] = 0

    return dict(calendar_data)

@app.route("/api/codeforces_calendar/<handle>")
def codeforces_calendar(handle):
    calendar_data = generate_calendar_data(handle)
    return jsonify(calendar_data)

if __name__ == "__main__":
    app.run(debug=True)
