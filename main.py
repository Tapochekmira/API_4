import requests
import os
import datetime
import telegram
import time
from pathlib import Path
from urllib.parse import urlparse
from dotenv import load_dotenv



def get_file_extension(picture_url):
    picture_path = urlparse(picture_url).path
    picture_tail = os.path.split(picture_path)[1] 
    picture_ext = os.path.splitext(picture_tail)[1]
    return picture_ext

    
def download_picture(directory, picture_name, url, api_key=None):
    payload = {
        'api_key': api_key
        }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    Path(directory).mkdir(parents=True, exist_ok=True)
    with open(f'{directory}{picture_name}', 'wb') as file:
        file.write(response.content)


def fetch_spacex_101_launch(directory):
    spasex_url = 'https://api.spacexdata.com/v3/launches/101/'
    spasex_response = requests.get(spasex_url)
    spasex_response.raise_for_status()
    spacex_pictures = spasex_response.json()['links']['flickr_images']
    for file_name, picture_url in enumerate(spacex_pictures):
        download_picture(directory, f'spacex{file_name}.jpeg', picture_url)


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
        download_picture(directory, f'nasa{picture_number}{get_file_extension(nasa_picture_url)}',
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

        picture_earth_url = f'https://api.nasa.gov/EPIC/archive/natural/{picture_earth_date}/png/{picture_earth_name}.png'
        download_picture(directory, f'EPIC{picture_number}.png', picture_earth_url, nasa_token)


def publish_text_to_telegram(telegram_token, directory, picture, chat_id):
    chat_id='@Kosmo_Super_Kek'
    bot = telegram.Bot(token=telegram_token)
    with open(f'{directory}{picture}', 'rb') as picture:
        bot.send_document(chat_id=chat_id, document=picture)


if __name__ == '__main__':
    load_dotenv()
    nasa_token = os.environ['NASA_TOKEN']
    telegram_token = os.environ['TELEGRAM_TOKEN']
    sleep_time = os.environ['SLEEP_TIME']
    chat_id = os.environ['CHAT_ID']
    directory = 'images/'
    numbers_of_pictures = 30
    wiki_url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"
    
    
    download_picture(directory, 'huble.jpeg', wiki_url)
    fetch_spacex_last_launch(directory)
    fetch_nasa_APOD(directory, numbers_of_pictures, nasa_token)
    fetch_nasa_EPIC(directory, nasa_token) 
    all_pictures = os.listdir(directory)
    
    for picture in all_pictures:
        publish_text_to_telegram(telegram_token, directory, picture, chat_id)
        time.sleep(int(sleep_time))
