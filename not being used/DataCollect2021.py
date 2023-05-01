import requests
import csv
from datetime import datetime, timedelta

# Set the start and end year for the data collection
year = 2021


# Set the range of dates to collect data for
start_date = datetime(year, 1, 1)
end_date = datetime(year, 1, 1)

# Set up the CSV file and headers
filename = f"top_100streamers{year}.csv"
with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['date', 'rank', 'username', 'viewer_count', 'game_name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate over each day and collect data
    date = start_date
    while date <= end_date:
        # Get an access token
        client_id = "j3y1cfszu2ptbntdp27n75hyqdqa9d"
        client_secret = "iks9011ul64k3fqez30t10dlb6x2se"
        token_url = "https://id.twitch.tv/oauth2/token"
        token_data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials"
        }
        token_response = requests.post(token_url, data=token_data)
        access_token = token_response.json()["access_token"]

        # Make a request to get the top 100 streamers
        headers = {
            "Client-ID": client_id,
            "Authorization": f"Bearer {access_token}"
        }
        url = f'https://api.twitch.tv/helix/streams?first=100&language=en&started_at={date.strftime("%Y-%m-%dT%H:%M:%SZ")}&ended_at={date.strftime("%Y-%m-%dT23:59:59Z")}'

        response = requests.get(url, headers=headers)
        top_100 = response.json()["data"]

        for i, streamer in enumerate(top_100):
            user_id = streamer['user_id']
            url = f"https://api.twitch.tv/helix/streams?user_id={user_id}"
            headers = {
                "Client-ID": client_id,
                "Authorization": f"Bearer {access_token}"
            }
            params = {
                "first": 1,
                "started_at": date.strftime('%Y-%m-%dT%H:%M:%SZ')
            }
            response = requests.get(url, headers=headers, params=params)
            data = response.json()["data"]
            if data:
                writer.writerow({
                    'date': date.strftime('%Y-%m-%d'),
                    'rank': i+1,
                    'username': data[0]['user_name'],
                    'viewer_count': data[0]['viewer_count'],
                    'game_name': data[0]['game_name']
                })
        date = date + timedelta(days=1)
        print(f"Data collected for {date.strftime('%Y-%m-%d')}")

print("Data collection complete!")
