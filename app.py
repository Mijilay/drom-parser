import os
import json
from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    brands = ["mercedes-benz", "bmw", "ford", "mazda", "peugeot"]
    return render_template('description_brand.html', brands=brands)

@app.route('/brand/<brand_name>')
def show_brand(brand_name):
    # Путь к директориям с JSON файлами и изображениями
    brands = ["mercedes-benz", "bmw", "ford", "mazda", "peugeot"]
    json_file_path = os.path.join(app.static_folder, 'cards', brand_name, 'cards_description.json')
    media_folder = os.path.join(app.static_folder, 'cards', brand_name, 'media')
    
    cars = []

    # Проверка на существование JSON файла
    if os.path.isfile(json_file_path):
        # Загружаем данные из JSON файла
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Обходим все автомобили в JSON файле
            for car in data:
                car_data = car.copy()  # Копируем данные для каждого автомобиля
                images = []
                
                # Формируем список изображений для каждого автомобиля
                if os.path.isdir(media_folder):
                    for media_file in os.listdir(media_folder):
                        if media_file.endswith(('.jpg', '.jpeg', '.png')):
                            # Проверка, чтобы связать правильные изображения с данными
                            count = car_data.get("count", "")
                            if media_file.startswith(f'{count}-'):
                                images.append(f'media/{brand_name}/{media_file}')
                
                car_data['images'] = images
                cars.append(car_data)

    return render_template('brand.html', brand_name=brand_name, cars=cars, brands=brands)

if __name__ == '__main__':
    app.run(debug=True)
