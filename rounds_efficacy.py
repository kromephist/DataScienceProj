import requests

# Replace YOUR_API_KEY with your actual API key
api_key = "RGAPI-bbf96d04-910e-4d6e-908e-d1185ebb7708"

# Set the API endpoint and match ID
endpoint = "https://api.valorant.riotgames.com/val/match/v1/matches/"
match_id = "MATCH_ID"

# Set the headers and query parameters
headers = {"X-Riot-Token": api_key}
params = {"matchId": match_id}

# Make the API request
response = requests.get(endpoint, headers=headers, params=params)

# Get the match data from the response JSON
match_data = response.json()

# Define a dictionary to store the win rates for each economy state
win_rates = {"save": 0, "eco": 0, "full_buy": 0, "force_buy": 0}

# Iterate through each round and calculate the win rate for each economy state
for round_data in match_data["info"]["roundResults"]:
    if round_data["roundCeremony"] == "CeremonyEconomy":
        economy_type = round_data["roundResult"]
        win_type = round_data["winType"]
        if win_type == "Elimination":
            win_rates[economy_type] += 1

# Calculate the total number of rounds for each economy state
total_rounds = sum(win_rates.values())

# Calculate the win rate for each economy state
for economy_type in win_rates:
    win_rates[economy_type] /= total_rounds
    win_rates[economy_type] *= 100

# Print the win rates for each economy state
print("Save win rate: ", win_rates["save"], "%")
print("Eco win rate: ", win_rates["eco"], "%")
print("Full buy win rate: ", win_rates["full_buy"], "%")
print("Force buy win rate: ", win_rates["force_buy"], "%")
