import os
import requests
import datetime
import time
import for_download_picture
from pathlib import Path
from urllib.parse import urlparse


def get_file_extension(picture_url):
    picture_path = urlparse(picture_url).path
    picture_tail = os.path.basename(picture_path)
    picture_ext = os.path.splitext(picture_tail)[1]
    return picture_ext


def fetch_nasa_APOD(directory, numbers_of_pictures, nasa_token):
    nasa_url = 'https://api.nasa.gov/planetary/apod'
    payload = {
        'api_key': nasa_token,
        'count': numbers_of_pictures,
        'thumbs': False
    }
    nasa_response = requests.get(nasa_url, params=payload)
    nasa_response.raise_for_status()
    nasa_apod_pictures = nasa_response.json()
    for picture_number, picture in enumerate(nasa_apod_pictures):
        nasa_picture_url = picture['url']
        for_download_picture.download_picture(directory,
                         (f'nasa{picture_number}'
                          + f'{get_file_extension(nasa_picture_url)}'),
                         nasa_picture_url)


def fetch_nasa_EPIC(directory, nasa_token):
    nasa_earth_url = 'https://api.nasa.gov/EPIC/api/natural/images'
    payload = {
        'api_key': nasa_token
    }
    nasa_earth_response = requests.get(nasa_earth_url, params=payload)
    nasa_earth_response.raise_for_status()

    nasa_earth_pictures = nasa_earth_response.json()
    for picture_number, picture in enumerate(nasa_earth_pictures):
        picture_earth_name = picture['image']
        picture_earth_date = picture['date']

        picture_earth_date = datetime.datetime.fromisoformat(picture_earth_date)
        picture_earth_date = picture_earth_date.strftime("%Y/%m/%d")

        picture_earth_url = (f'https://api.nasa.gov/EPIC/archive/natural/'
                             + f'{picture_earth_date}/png/'
                             + f'{picture_earth_name}.png')
        for_download_picture.download_picture(directory, f'EPIC{picture_number}.png',
                         picture_earth_url, nasa_token)
