import requests
from pathlib import Path

def download_picture(directory, picture_name, url, api_key=None):
    payload = {
        'api_key': api_key
        }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    with open(f'{directory}{picture_name}', 'wb') as file:
        file.write(response.content)
