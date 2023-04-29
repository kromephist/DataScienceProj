import requests

def get_match_ids(tournament_code):
    """
    Given a tournament code, returns a list of match IDs for that tournament
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer API_KEY'
    }

    # Get the tournament ID from the tournament code
    url = f'https://api.pandascore.co/valorant/tournaments?filter[url]={tournament_code}'
    response = requests.get(url, headers=headers)
    tournament_id = response.json()[0]['id']

    # Get the list of match IDs for the tournament
    url = f'https://api.pandascore.co/valorant/matches?filter[tournament_id]={tournament_id}'
    response = requests.get(url, headers=headers)
    match_ids = [match['id'] for match in response.json()]

    return match_ids
