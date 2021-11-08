import requests
import os
import datetime
import telegram
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


def fetch_spacex_last_launch(directory):
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
    'count': 30,
    'thumbs': False
    }
    nasa_response = requests.get(nasa_url, params=payload)
    nasa_response.raise_for_status()
    for picture_number in range(numbers_of_pictures):
        nasa_picture_url = nasa_response.json()[picture_number]['url']
        download_picture(directory, f'nasa{picture_number}{get_file_extension(nasa_picture_url)}',
                         nasa_picture_url)


def fetch_nasa_EPIC(directory, nasa_token):
    nasa_earth_url = 'https://api.nasa.gov/EPIC/api/natural/images'
    payload = {
        'api_key': nasa_token
        }
    nasa_earth_response = requests.get(nasa_earth_url, params=payload)
    nasa_earth_response.raise_for_status()
    
    nasa_earth_picture = nasa_earth_response.json()
    for number in range(len(nasa_earth_picture) // 2):
        picture_earth_name = nasa_earth_picture[number]['image']
        picture_earth_date = nasa_earth_picture[number]['date']

        picture_earth_date = datetime.datetime.fromisoformat(picture_earth_date)
        picture_earth_date = picture_earth_date.strftime("%Y/%m/%d")

        picture_earth_url = f'https://api.nasa.gov/EPIC/archive/natural/{picture_earth_date}/png/{picture_earth_name}.png'
        download_picture(directory, f'EPIC{number}.png', picture_earth_url, nasa_token)


def publish_text_to_telegram(telegram_token):
    bot = telegram.Bot(token=telegram_token)
    bot.send_message(chat_id='@Kosmo_Super_Kek', text="I'm sorry Dave I'm afraid I can't do that.")
    

    
if __name__ == '__main__':
    load_dotenv()
    nasa_token = os.environ['NASA_TOKEN']
    telegram_token = os.environ['TELEGRAM_TOKEN']

    directory = 'images/'
    numbers_of_pictures = 30
    wiki_url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"
    
    
#    download_picture(directory, 'huble.jpeg', wiki_url)
#    fetch_spacex_last_launch(directory)
#    fetch_nasa_APOD(directory, numbers_of_pictures, nasa_token)
#    fetch_nasa_EPIC(directory, nasa_token) 

    publish_text_to_telegram(telegram_token)