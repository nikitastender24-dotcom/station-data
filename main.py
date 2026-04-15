#!/usr/bin/env python3
"""
Погодный сервер на Flask (порт 8080)
Отдаёт HTML-страницу с картой и проксирует запросы к API ГГО им. Воейкова
"""

from flask import Flask, send_from_directory, request, jsonify
import requests

app = Flask(__name__, static_folder='.', static_url_path='')

# Маршрут для главной страницы
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Прокси для API ГГО – забирает данные с сервера Воейкова и возвращает клиенту
@app.route('/api/weather')
def proxy_weather():
    base_url = "https://cc.voeikovmgo.ru/iframes/cwt/get-kn01.php"
    params = {
        "bounds": request.args.get("bounds", "-180,-90,180,90"),
        "zoom": request.args.get("zoom", "4"),
        "datetime": request.args.get("datetime", "now"),
        "lang": request.args.get("lang", "ru"),
        "layer": request.args.get("layer", "puasson"),
        "actuality": request.args.get("actuality", "240")
    }
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(base_url, params=params, headers=headers, timeout=30)
    return jsonify(resp.json()), resp.status_code

if __name__ == '__main__':
    print("🌍 Запуск погодного сервера на http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)
