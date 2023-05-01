import requests
import json

# Replace 'YOUR_API_KEY' with a valid Twitch API key
client_id = "j3y1cfszu2ptbntdp27n75hyqdqa9d"
client_secret = "iaam7paa6gvve7uvwirkuohzsuekug"

# Set up the headers for the API request
headers = {
    'Client-ID': client_id,
    'Client-Secret': client_secret,
    'Accept': 'application/vnd.twitchtv.v5+json'
}

# Set up the base URL for the API requests
base_url = 'https://api.twitch.tv/kraken/'

# Define a function to get the total viewership for a single channel
def get_channel_viewers(channel):
    url = base_url + 'streams/{}'.format(channel)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = json.loads(response.text)
        if data['stream'] is not None:
            return data['stream']['viewers']
        else:
            return 0
    else:
        print(response.status_code)
        return None

# Define a function to get the total viewership for a single game
def get_game_viewers(game):
    url = base_url + 'streams/?game={}'.format(game)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = json.loads(response.text)
        total_viewers = 0
        for stream in data['streams']:
            total_viewers += stream['viewers']
        return total_viewers
    else:
        print(response.status_code)
        return None

# Define a list of channels and games to track
channels = ['LIRIK', 'shroud', 'ninja']
games = ['League of Legends', 'Fortnite', 'Valorant']

# Set up a dictionary to store the total viewership for each channel and game
channel_viewers = {}
game_viewers = {}

# Gather data over a period of time (e.g. 24 hours)
for i in range(24):
    # Get the current time (in hours)
    current_time = i % 24

    # Set up a dictionary to store the total viewership for each channel and game at the current time
    current_channel_viewers = {}
    current_game_viewers = {}

    # Get the total viewership for each channel and game
    for channel in channels:
        current_channel_viewers[channel] = get_channel_viewers(channel)
    for game in games:
        current_game_viewers[game] = get_game_viewers(game)

    # Add the current viewership data to the overall data for the day
    for channel, viewers in current_channel_viewers.items():
        if channel not in channel_viewers:
            channel_viewers[channel] = []
        channel_viewers[channel].append((current_time, viewers))
    for game, viewers in current_game_viewers.items():
        if game not in game_viewers:
            game_viewers[game] = []
        game_viewers[game].append((current_time, viewers))

# Print the total viewership data for each channel and game
print('Channel viewership over time:')
for channel, data in channel_viewers.items():
    print(channel)
    for time, viewers in data:
        print('{}: {}'.format(time, viewers))
print('')

print('Game viewership over time:')
for game, data in game_viewers.items():
    print(game)
    for time, viewers in data:
        print('{}: {}'.format(time, viewers))
