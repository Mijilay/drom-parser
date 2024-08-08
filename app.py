from flask import Flask, render_template
from livereload import Server

app = Flask(__name__)
app.debug = True

@app.route('/')
def home():
    return render_template('index.html')

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
