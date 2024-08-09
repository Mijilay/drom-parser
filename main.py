import requests
import json
import os.path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path

def get_cars_cards():
    url = f'https://spb.drom.ru/mercedes-benz/all/'
    params = {"ph": 1, 
            "unsold": 1}
    response = requests.get(url, params=params)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    cards_tag = soup.find(class_="css-1nvf6xk ejck0o60").find_all(class_='css-1f68fiz ea1vuk60')


    for number, card in enumerate(cards_tag):
        link_tag = card.find(class_="css-10vnevh e1pqv6mt0").find_all("a")
        for link in link_tag:
            car_link = link.get("href")
        
        image_tag = card.find(class_="emt6rd0 css-ac6cb6 e4lamf0").find("img")
        image_link = image_tag.get("src")
        filename = f'mercedes-benz{number}.jpg'
        download_images(image_link, filename)


def download_images(image_link, filename, folder="cars_image"):
    response = requests.get(image_link)
    response.raise_for_status()
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)



def main():
    Path("cars_image").mkdir(parents=True, exist_ok=True)
    #cars = ['mercedes-benz', 'tesla', 'ford', 'bmw', 'kia']

    #for car in cars:

    cards = get_cars_cards()


if __name__ == "__main__":
    main()