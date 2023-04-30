import requests

client_id = "j3y1cfszu2ptbntdp27n75hyqdqa9d"
client_secret = "ewx95jgrov0mxp4nrkhs7kbfi1oc6z"

# Get an access token
token_url = "https://id.twitch.tv/oauth2/token"
token_data = {
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": "client_credentials"
}
token_response = requests.post(token_url, data=token_data)
access_token = token_response.json()["access_token"]

# Make a request to get the top 5 streamers by viewership
headers = {
    "Client-ID": client_id,
    "Authorization": f"Bearer {access_token}"
}
url = "https://api.twitch.tv/helix/streams?first=5&language=en"
response = requests.get(url, headers=headers)
top_5 = response.json()["data"]

url = "https://api.twitch.tv/helix/games/top?first=5"
response = requests.get(url, headers=headers)
top_5_games = response.json()["data"]

# Print the top 5 streamers
for i, streamer in enumerate(top_5):
    print(f"{i+1}. {streamer['user_name']} - {streamer['viewer_count']} viewers")

print("\nTop 5 Games:")
for i, game in enumerate(top_5_games):
    game_id = game["id"]
    game_name = game["name"]
    streams_url = f"https://api.twitch.tv/helix/streams?game_id={game_id}"
    streams_response = requests.get(streams_url, headers=headers)
    streams = streams_response.json()["data"]
    total_viewers = sum([stream["viewer_count"] for stream in streams])
    print(f"{i+1}. {game_name} - {total_viewers} viewers")
