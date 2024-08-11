import requests
import json
import os.path
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup
from pathlib import Path

def get_cars_cards(response, car, count):
    soup = BeautifulSoup(response.text, 'lxml')
    cards_tag = soup.find_all(class_='css-1f68fiz ea1vuk60')

    for number, card in enumerate(cards_tag):
        link_tag = card.find(class_="css-10vnevh e1pqv6mt0").find("a")
        car_link = link_tag.get("href")
            
        image_tag = card.find(class_="emt6rd0 css-ac6cb6 e4lamf0").find("img")
        image_link = image_tag.get("src")
        expansion_link = get_expansion_link(image_link)

        filename = f'{car}{count}-{number}{expansion_link}'
        download_images(image_link, filename, folder=f"static/media/{car}")

        cards_title = card.find_all(class_="g6gv8w4 g6gv8w8 _1ioeqy90")
        car_model, car_year = cards_title[0].get_text().split(", ")

        cars_price  = card.find_all(class_="css-1dv8s3l eyvqki91")

        cards_text = card.find_all(class_= "css-1l9tp44 e162wx9x0")

        if 5 == len(cards_text):
            cards = {
                "link": car_link,
                "image": filename,
                "model": car_model,
                "year": car_year,
                "price:": cars_price[0].get_text(),
                "hp": cards_text[0].get_text(),
                "engine": cards_text[1].get_text(),
                "transmission": cards_text[2].get_text(),
                "drive": cards_text[3].get_text(),
                "mileage": cards_text[4].get_text()
            }
        elif 4 == len(cards_text):
            cards = {
                "link": car_link,
                "image": filename,
                "model": car_model,
                "year": car_year,
                "price:": cars_price[0].get_text(),
                "hp": cards_text[0].get_text(),
                "engine": cards_text[1].get_text(),
                "transmission": cards_text[2].get_text(),
                "drive": cards_text[3].get_text()
            }
        else:
            cards = {
                "link": car_link,
                "image": filename,
                "model": car_model,
                "year": car_year,
                "price": cars_price[0].get_text(),
                "engine": cards_text[0].get_text(),
                "transmission": cards_text[1].get_text(),
                "drive": cards_text[2].get_text(),    
            }
            

def get_expansion_link(link):
    path_image = urlsplit(unquote(link)).path
    path, full_file_name = os.path.split(path_image)
    file_name, expansion = os.path.splitext(full_file_name)
    return expansion


def download_images(image_link, filename, folder):
    response = requests.get(image_link)
    response.raise_for_status()
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def main():
    Path("static/media").mkdir(parents=True, exist_ok=True)
    cars_model = ['mercedes-benz', 'peugeot', 'ford', 'bmw', 'mazda']

    for car in cars_model: 
        os.makedirs(f'static/media/{car}', exist_ok=True)
        os.makedirs(f"static/cards/{car}", exist_ok=True)

        url_for_pages = f'https://spb.drom.ru/{car}/all/'
        params = {"ph": 1, 
                "unsold": 1}
        response = requests.get(url_for_pages, params=params)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        pages_tag = soup.find_all(class_="css-14yriw2 e1px31z30")[1]
        pages_quantity = int(pages_tag.get_text().split()[0]) // 20 + 1
        print(pages_quantity)

        for count in range(1, pages_quantity+1):
            url = f'https://spb.drom.ru/{car}/all/page{count}/'
            params = {"ph": 1, 
                    "unsold": 1}
            response = requests.get(url, params=params)
            response.raise_for_status()

            get_cars_cards(response, car, count)


if __name__ == "__main__":
    main()