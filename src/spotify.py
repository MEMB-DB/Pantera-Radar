import requests

def get_spotify_token(client_id,client_secret, refresh_token):
    """Request a temporary Spotify access token (valid for 1 hour) using the permanent refresh token."""
  
    payload={'grant_type':'refresh_token', 'client_id': client_id, 'client_secret': client_secret, 'refresh_token': refresh_token}

    r= requests.post(url="https://accounts.spotify.com/api/token",data=payload, timeout=10)

    if (r.status_code==200):
    
        token=r.json().get("access_token")
        return token
    
    else:
        print(f"ERROR TOKEN CODE {r.status_code}")
        return None
    

def fetch_spotify_artists(token, limit):
    """Fetch the user's top listened artists from Spotify (up to 'limit' artists)."""

    # Guard clause: abort immediately if authentication failed and no token is available
    if token==None:
        return []

    payload={'time_range': 'short_term', 'limit': limit, 'offset': 0}
    header={'Authorization': f'Bearer {token}'}

    r= requests.get(url="https://api.spotify.com/v1/me/top/artists",headers=header, params=payload, timeout=10)

    if(r.status_code==200):
        
        artists= (r.json().get("items") or [])
        return artists
    
    else:
        print(f"CALL ERROR CODE {r.status_code}")
        return []

    
def transform_artists(artists):
    """Extract clean artist names (strings) from the raw Spotify artist dictionaries."""
    cleaned=[]

    for artist in artists:
        if artist.get("name") != None:
            cleaned.append(artist.get("name"))

    return cleaned
