import requests
from bs4 import BeautifulSoup

def get_cars_cards(response):
    soup = BeautifulSoup(response.text, 'lxml')



def main():
    cars = ['mercedes-benz', 'tesla', 'ford', 'bmw', 'kia']

    for car in cars:
        url = f'https://spb.drom.ru/{car}/all/'
        params = {"ph": 1, 
                  "unsold": 1}
        response = requests.get(url, params=params)
        response.raise_for_status()
        print(response.text)

        get_cars_cards(response)


if __name__ == "__main__":
    main()