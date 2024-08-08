import requests
import json
from bs4 import BeautifulSoup

def get_cars_cards(response):
    soup = BeautifulSoup(response.text, 'lxml')
    cards_tag = soup.find(class_="css-1nvf6xk ejck0o60").find_all(class_='css-1f68fiz ea1vuk60')


    for card in cards_tag:
        link_tag = card.find(class_="css-10vnevh e1pqv6mt0").find_all("a")
        for link in link_tag:
            car_link = link.get("href")





def main():
    #cars = ['mercedes-benz', 'tesla', 'ford', 'bmw', 'kia']

    #for car in cars:
        url = f'https://spb.drom.ru/mercedes-benz/all/'
        params = {"ph": 1, 
                  "unsold": 1}
        response = requests.get(url, params=params)
        response.raise_for_status()

        cards = get_cars_cards(response)
        # download_images(response, cards)

if __name__ == "__main__":
    main()