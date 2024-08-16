import requests
import json
import os.path
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup
from itertools import count

def get_cars_cards(response, car, count, cards_list):
    soup = BeautifulSoup(response.text, 'lxml')
    cards_tag = soup.find(attrs={"data-bulletin-list": "true"}).find_all(class_='css-1f68fiz ea1vuk60')

    for number, card in enumerate(cards_tag):
        link_tag = card.find("a")
        car_link = link_tag.get("href")
            
        image_tag = card.find(class_="emt6rd0 css-ac6cb6 e4lamf0").find("img")
        image_link = image_tag.get("src")
        expansion_link = get_expansion_link(image_link)

        filename = f'{count}-{number}{expansion_link}'
        download_images(image_link, filename, folder=f"static/cards/{car}/media")

        cards_title = card.find_all(class_="g6gv8w4 g6gv8w8 _1ioeqy90")
        car_model, car_year = cards_title[0].get_text().split(", ")

        cars_price  = card.find_all(class_="css-1dv8s3l eyvqki91")

        cards_text = card.find_all(class_= "css-1l9tp44 e162wx9x0")

        card_text = []

        for text in cards_text:
            card_text.append(text.text)
        

        cards_list.append({
                "link": car_link,
                "image": filename,
                "model": car_model,
                "year": car_year,
                "price": cars_price[0].text,
                "card_description": card_text
            })
        
    return cards_list
            

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


def get_json_files(cards, folder):
    with open(folder, 'w+', encoding='utf8') as file:
        json.dump(cards, file, ensure_ascii=False, indent=4)


def main():
    cars_model = ['mercedes-benz', 'peugeot', 'ford', 'bmw', 'mazda']

    for car in cars_model:
        os.makedirs(f'static/cards/{car}/media', exist_ok=True)

        cards_list = []

        for page in count(1, 1):
            url = f'https://spb.drom.ru/{car}/all/page{page}/'
            params = {"ph": 1, 
                    "unsold": 1}
            response = requests.get(url, params=params)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            caar = soup.find(attrs={'data-ftid': "bulletin-list_nearby"})
            cards = get_cars_cards(response, car, page, cards_list)
            if caar:
                break

            
            

        get_json_files(cards, folder=f"static/cards/{car}/cards_description.json")


if __name__ == "__main__":
    main()