from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# GETTING THE HOT 100 BILLBOARD
date = input("Which date (YYYY-MM-DD) top 100 would you like to reach: ")
bb_response = requests.get(url=f"https://www.billboard.com/charts/hot-100/" + date)
songs = bb_response.text
soup = BeautifulSoup(songs,"html.parser")
top_100 = soup.select("li h3")
# Strip() alone, gets hold of only the string text
titles = [items.getText().strip() for items in top_100]

# SPOTIFY AUTHENTICATION
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('CLIENT_ID'),
                                               client_secret=os.getenv('CLIENT_SECRET'),
                                               redirect_uri="http://example.com",
                                               cache_path="token.txt",
                                               scope="playlist-modify-private",
                                               username="Dstv"))

# CREATING THE LIST OF URIS FROM THE SONGS
user_id = sp.current_user()["id"]
uris = []
year = date[:4]
for item in titles:
    try:
        info = sp.search(q=f"track:{item} year:{year}", type="track")
        uri = info['tracks']['items'][0]['uri']
        uris.append(uri)
    except IndexError:
        print(f"{item} does not exist on spotify's library, skipped")

# CREATE A PLAYLIST AND ADD THE SONGS
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=(playlist["id"]), items=uris)
