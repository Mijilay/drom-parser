from flask import Flask, render_template
from livereload import Server
import os

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    image_folder = os.path.join(app.static_folder, 'cars_image')
    imgs = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    return render_template('index.html', imgs=imgs)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    # Создаем сервер LiveReload
    server = Server(app.wsgi_app)
    
    # Папка где находятся шаблоны и статические файлы
    server.watch('templates')
    server.watch('static')
    
    # Запускаем сервер
    server.serve(port=5000)
