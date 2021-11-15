import os
import telegram
import fetch_nasa
import fetch_spacex
from pathlib import Path
from dotenv import load_dotenv


def publish_text_to_telegram(telegram_token, directory, picture, chat_id):
    chat_id = '@Kosmo_Super_Kek'
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
    
    Path(directory).mkdir(parents=True, exist_ok=True)
    fetch_spacex.fetch_spacex_101_launch(directory)
    fetch_nasa.fetch_nasa_APOD(directory, numbers_of_pictures, nasa_token)
    fetch_nasa.fetch_nasa_EPIC(directory, nasa_token)
    all_pictures = os.listdir(directory)

    for picture in all_pictures:
        publish_text_to_telegram(telegram_token, directory, picture, chat_id)
        time.sleep(int(sleep_time))
