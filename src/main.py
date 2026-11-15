from spotify import get_spotify_token, fetch_spotify_artists, transform_artists
from ticketmaster import fetch_ticketmaster_events, transform_events

from dotenv import load_dotenv

import os

load_dotenv()

# Number of top listened artists to retrieve from Spotify and process in the pipeline
limit= 15


def main():
    """Orchestrate the pipeline: fetch top Spotify artists and search their live events on Ticketmaster."""

    spotify_client_id= os.environ["SPOTIFY_CLIENT_ID"]
    spotify_client_secret= os.environ["SPOTIFY_CLIENT_SECRET"]
    spotify_refresh_token= os.environ["SPOTIFY_REFRESH_TOKEN"]

    # 1. Authenticate and fetch raw top artist objects from Spotify
    token= get_spotify_token(spotify_client_id,spotify_client_secret,spotify_refresh_token)

    artists= fetch_spotify_artists(token, limit)

    # 2. Extract only the artist names (strings) from the raw Spotify dictionaries
    artist_names= transform_artists(artists)

    ticketmaster_api_key = os.environ["TICKETMASTER_KEY"]

    # 3. Search and clean live events on Ticketmaster for each artist name
    for artist in artist_names:
        events= fetch_ticketmaster_events(ticketmaster_api_key,artist)
        cleaned=transform_events(events)
        print(artist,cleaned)


if __name__ == "__main__":
    main()
