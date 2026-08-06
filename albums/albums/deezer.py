import requests

DEEZER_ALBUM_URL = "https://api.deezer.com/album/{}"

def get_album(deezer_id):
    response = requests.get(DEEZER_ALBUM_URL.format(deezer_id))
    if response.status_code == 200:
        return response.json()
    return None