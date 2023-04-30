import requests
import json
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import time
def calculate_efficacy(match_ids):
    """
    Given a list of match IDs, returns a list of dictionaries containing the efficacy values
    for each team in each match.
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 8YfkVAHA7EBEwzAr86TOYJbZ88fpmQmMoYXqf6DTACw7BiS5Nuw'
    }

    # Initialize the list of dictionaries
    efficacy_data = []

    # Loop over each match ID
    for match_id in match_ids:
        # Get the data for the match
        url = f'https://api.pandascore.co/valorant/matches/{match_id}'
        response = requests.get(url, headers=headers)
        data = response.json()

        # Get the ID and name of each team
        team_ids = [team['id'] for team in data['opponents']]
        team_names = [team['name'] for team in data['opponents']]
       
        # Loop over each team
        for i, team_id in enumerate(team_ids):
            # Get the round data for the team
            url = f'https://api.pandascore.co/valorant/matches/{match_id}/rounds?filter[team_id]={team_id}'
            response = requests.get(url, headers=headers)
            data = response.json()
            
            # Calculate the efficacy values for the team
            save_eff = sum([round['player_stats']['round_stats']['is_defuse'] for round in data]) / len(data)
            eco_eff = sum([round['player_stats']['round_stats']['is_first_kill'] for round in data]) / len(data)
            buy_eff = sum([round['player_stats']['round_stats']['is_first_death'] for round in data]) / len(data)

            # Add the efficacy data to the list of dictionaries
            efficacy_data.append({'match_id': match_id, 'team_id': team_id, 'team_name': team_names[i],
                                  'save_eff': save_eff, 'eco_eff': eco_eff, 'buy_eff': buy_eff})

    # Scale the efficacy data using min-max scaling
    efficacy_df = pd.DataFrame(efficacy_data)
    scaler = MinMaxScaler()
    efficacy_df[['save_eff', 'eco_eff', 'buy_eff']] = scaler.fit_transform(efficacy_df[['save_eff', 'eco_eff', 'buy_eff']])
    efficacy_data = efficacy_df.to_dict('records')

    return efficacy_data
