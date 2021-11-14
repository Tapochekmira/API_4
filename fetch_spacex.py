import requests
import for_download_picture


def fetch_spacex_101_launch(directory):
    spasex_url = 'https://api.spacexdata.com/v3/launches/101/'
    spasex_response = requests.get(spasex_url)
    spasex_response.raise_for_status()
    spacex_pictures = spasex_response.json()['links']['flickr_images']
    for file_name, picture_url in enumerate(spacex_pictures):
        for_download_picture.download_picture(directory,
                                              f'spacex{file_name}.jpeg', picture_url)
