import requests

def get_match_ids(tournament_name):
    """
    Given a tournament name, returns a list of match IDs for that tournament
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 8YfkVAHA7EBEwzAr86TOYJbZ88fpmQmMoYXqf6DTACw7BiS5Nuw'
    }

    API_KEY = '8YfkVAHA7EBEwzAr86TOYJbZ88fpmQmMoYXqf6DTACw7BiS5Nuw'



    url = f'https://api.pandascore.co/tournaments?filter[slug]={tournament_name}&token={API_KEY}'
    response = requests.get(url)

    if not response.json():
        return []

    # Get the tournament ID from the tournament name
    url = f'https://api.pandascore.co/valorant/tournaments?filter[url]={tournament_name}'
    response = requests.get(url, headers=headers)
    tournament_id = response.json()[0]['id']

    # Get the list of match IDs for the tournament
    url = f'https://api.pandascore.co/valorant/matches?filter[tournament_id]={tournament_id}'
    response = requests.get(url, headers=headers)

    
    match_ids = [match['id'] for match in response.json()]

    return match_ids
