import os
import json
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Список марок автомобилей
    brands = ["mercedes-benz", "bmw", "ford", "mazda", "peugeot"]
    
    return render_template('description_brand.html', brands=brands)

@app.route('/brand/<brand_name>')
def show_brand(brand_name):
    # Путь к директориям с изображениями и текстовыми файлами
    brands = ["mercedes-benz", "bmw", "ford", "mazda", "peugeot"]
    text_folder = os.path.join(app.static_folder, 'cards', brand_name)
    
    cars = []

    if os.path.isdir(text_folder):
        for txt_file in os.listdir(text_folder):
            if txt_file.endswith('.txt'):
                # Путь к текстовому файлу
                txt_file_path = os.path.join(text_folder, txt_file)
                
                # Загружаем данные из текстового файла
                with open(txt_file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Добавляем путь к изображению в данные
                    image_name = data.get("image")
                    if image_name:
                        # Используем url_for для корректного формирования пути
                        data['image'] = f'media/{brand_name}/{image_name}'
                    cars.append(data)

    return render_template('brand.html', brand_name=brand_name, cars=cars, brands=brands)

if __name__ == '__main__':
    app.run(debug=True)
